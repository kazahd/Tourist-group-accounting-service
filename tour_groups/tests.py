"""Проверки Django-моделей, ORM-представлений и административной панели."""
import base64
from datetime import date
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .forms import ParticipantForm, TripForm, TripFilterForm
from .models import Group, Participant, Trip


class TouristServiceTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(
            name="Поход на Алтай", route="Алтай", max_capacity=12
        )

    def test_group_get_absolute_url_uses_generated_slug(self):
        self.assertTrue(self.group.slug)
        self.assertEqual(
            self.group.get_absolute_url(),
            reverse("tour_groups:detail", kwargs={"slug": self.group.slug}),
        )

    def test_participant_adult_flag_is_generated_from_age(self):
        adult = Participant.objects.create(
            name="Анна", age=18, group=self.group
        )
        child = Participant.objects.create(
            name="Илья", age=17, group=self.group
        )
        adult.refresh_from_db()
        child.refresh_from_db()
        self.assertTrue(adult.is_adult)
        self.assertFalse(child.is_adult)

    def test_trip_queryset_status_methods_and_custom_manager(self):
        active = Trip.objects.create(
            group=self.group, trip_date=date(2027, 6, 1)
        )
        cancelled = Trip.objects.create(
            group=self.group,
            trip_date=date(2027, 6, 2),
            status=Trip.Status.CANCELLED,
        )
        self.assertEqual(list(Trip.objects.active()), [active])
        self.assertEqual(list(Trip.objects.cancelled()), [cancelled])
        self.assertEqual(
            list(Trip.objects.for_date(date(2027, 6, 1))), [active]
        )

    def test_trip_list_filters_by_status_and_group(self):
        Trip.objects.create(group=self.group, trip_date=date(2027, 6, 1))
        Trip.objects.create(
            group=self.group,
            trip_date=date(2027, 6, 2),
            status=Trip.Status.CANCELLED,
        )
        response = self.client.get(
            reverse("tour_trips:list"),
            {"status": Trip.Status.CANCELLED, "group": "Алтай"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].paginator.count, 1)

    def test_trip_filter_form_validates_date_range(self):
        form = TripFilterForm({
            "date_from": "2027-06-20",
            "date_to": "2027-06-01",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_trip_list_supports_legacy_from_to_get_parameters(self):
        trip = Trip.objects.create(
            group=self.group, trip_date=date(2027, 6, 5)
        )
        response = self.client.get(reverse("tour_trips:list"), {
            "from": "2027-06-01",
            "to": "2027-06-10",
        })
        results = list(response.context["page_obj"].object_list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], trip)

    def test_group_statistics_use_values_and_values_list(self):
        Participant.objects.create(name="Алиса", age=24, group=self.group)
        empty_group = Group.objects.create(
            name="Пустая группа", route="Урал", max_capacity=5
        )
        response = self.client.get(reverse("tour_groups:stats"))
        self.assertEqual(response.status_code, 200)
        rows = list(response.context["stats"])
        self.assertEqual(rows[0]["name"], self.group.name)
        self.assertEqual(rows[0]["participants_count"], 1)
        self.assertEqual(
            list(response.context["empty_groups"]), [empty_group.name]
        )

    def test_participant_delete_is_post_only_and_group_scoped(self):
        participant = Participant.objects.create(
            name="Удаляемый", age=20, group=self.group
        )
        remove_url = reverse(
            "tour_groups:participant_remove",
            args=[self.group.slug, participant.pk],
        )
        self.assertEqual(self.client.get(remove_url).status_code, 405)
        response = self.client.post(remove_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Participant.objects.filter(pk=participant.pk).exists()
        )

    def test_group_delete_sets_participant_group_null_and_cascades_trips(self):
        participant = Participant.objects.create(
            name="Оставшийся", age=20, group=self.group
        )
        trip = Trip.objects.create(
            group=self.group, trip_date=date(2027, 8, 1)
        )
        self.group.delete()
        participant.refresh_from_db()
        self.assertIsNone(participant.group_id)
        self.assertFalse(Trip.objects.filter(pk=trip.pk).exists())

    def test_trip_edit_uses_instance_and_saves_updated_values(self):
        trip = Trip.objects.create(
            group=self.group, trip_date=date(2027, 8, 1)
        )
        response = self.client.post(
            reverse("tour_trips:update", args=[trip.pk]),
            {
                "group": self.group.pk,
                "trip_date": "2027-08-02",
                "status": Trip.Status.ACTIVE,
            },
        )
        trip.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(trip.trip_date, date(2027, 8, 2))

    def test_trip_form_rejects_duplicate_date_but_allows_editing_self(self):
        trip = Trip.objects.create(
            group=self.group, trip_date=date(2027, 6, 1)
        )
        duplicate = TripForm({
            "group": self.group.pk,
            "trip_date": "2027-06-01",
            "status": Trip.Status.ACTIVE,
        })
        self.assertFalse(duplicate.is_valid())
        edit = TripForm({
            "group": self.group.pk,
            "trip_date": "2027-06-01",
            "status": Trip.Status.ACTIVE,
        }, instance=trip)
        self.assertTrue(edit.is_valid(), edit.errors)

    def test_participant_form_enforces_group_capacity(self):
        self.group.max_capacity = 1
        self.group.save()
        Participant.objects.create(
            name="Уже записан", age=30, group=self.group
        )
        form = ParticipantForm({"name": "Новый", "age": 20}, group=self.group)
        self.assertFalse(form.is_valid())
        self.assertIn("В группе нет свободных мест.", form.non_field_errors())

    def test_trip_create_post_persists_valid_model_form(self):
        response = self.client.post(reverse("tour_trips:create"), {
            "group": self.group.pk,
            "trip_date": "2027-07-10",
            "status": Trip.Status.ACTIVE,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Trip.objects.filter(
                group=self.group, trip_date=date(2027, 7, 10)
            ).exists()
        )

    def test_trip_create_invalid_post_shows_field_errors(self):
        Trip.objects.create(group=self.group, trip_date=date(2027, 7, 10))
        response = self.client.post(reverse("tour_trips:create"), {
            "group": self.group.pk,
            "trip_date": "2027-07-10",
            "status": Trip.Status.ACTIVE,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "У этой группы уже запланирована поездка"
        )

    def test_group_form_accepts_multipart_upload(self):
        tiny_gif = base64.b64decode(
            "R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
        )
        upload = SimpleUploadedFile(
            "route.gif", tiny_gif, content_type="image/gif"
        )
        with TemporaryDirectory() as media_dir:
            with override_settings(MEDIA_ROOT=media_dir):
                response = self.client.post(reverse("tour_groups:create"), {
                    "name": "Новый маршрут",
                    "route": "Карелия",
                    "max_capacity": 8,
                    "image": upload,
                })
        self.assertEqual(response.status_code, 302)
        group = Group.objects.get(name="Новый маршрут")
        self.assertTrue(group.image.name.startswith("groups/"))

    def test_trip_cancel_requires_post_and_changes_status(self):
        trip = Trip.objects.create(
            group=self.group, trip_date=date(2027, 7, 10)
        )
        cancel_url = reverse("tour_trips:cancel", args=[trip.pk])
        self.assertEqual(self.client.get(cancel_url).status_code, 405)
        response = self.client.post(cancel_url)
        trip.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(trip.status, Trip.Status.CANCELLED)

    def test_post_forms_include_csrf_token(self):
        response = self.client.get(reverse("tour_trips:create"))
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'method="post"')

    def test_csrf_rejects_tokenless_form_post(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse("tour_trips:create"), {
            "group": self.group.pk,
            "trip_date": "2027-07-10",
            "status": Trip.Status.ACTIVE,
        })
        self.assertEqual(response.status_code, 403)

    def test_trip_form_past_date_requires_completed_status(self):
        past_date = date(2020, 1, 1)
        active = TripForm({
            "group": self.group.pk,
            "trip_date": past_date.isoformat(),
            "status": Trip.Status.ACTIVE,
        })
        completed = TripForm({
            "group": self.group.pk,
            "trip_date": past_date.isoformat(),
            "status": Trip.Status.COMPLETED,
        })
        self.assertFalse(active.is_valid())
        self.assertIn("trip_date", active.errors)
        self.assertTrue(completed.is_valid(), completed.errors)

    def test_admin_lists_and_group_inline_are_available(self):
        user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="pass12345"
        )
        self.client.force_login(user)
        changelist = self.client.get(
            reverse("admin:tour_groups_group_changelist")
        )
        changeform = self.client.get(
            reverse("admin:tour_groups_group_change", args=[self.group.pk])
        )
        self.assertEqual(changelist.status_code, 200)
        self.assertEqual(changeform.status_code, 200)
        self.assertContains(changeform, "Участники")
        self.assertContains(changeform, "Поездки")
