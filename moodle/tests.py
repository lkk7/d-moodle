from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

from .models import Course, Lesson, Question
from .forms import LessonAddForm, QuestionAskForm


def create_example_course():
    teacher_1 = User.objects.create_user(
        username='teacher_1', password='12345')
    teacher_2 = User.objects.create_user(
        username='teacher_2', password='12345')
    student_1 = User.objects.create_user(
        username='student_1', password='12345')
    student_2 = User.objects.create_user(
        username='student_2', password='12345')
    teachers_group = Group.objects.create(name='Teachers')
    students_group = Group.objects.create(name='Students')
    teachers_group.user_set.add(teacher_1, teacher_2)
    students_group.user_set.add(student_1, student_2)
    course = Course.objects.create(name="A Course")
    course.teachers.set((teacher_1, teacher_2))
    course.students.set((student_1, student_2))
    return course


def create_example_lesson():
    course = create_example_course()
    return Lesson.objects.create(title="A Lesson", course=course,
                                 text="Qwerty, abc.")


def create_example_question():
    course = create_example_course()
    lesson = Lesson.objects.create(course=course, title='A Lesson')
    asker = User.objects.get(username='student_1')
    return Question.objects.create(asker=asker, lesson=lesson,
                                   text="How to do this?")


def force_login_student(instance):
    instance.client.force_login(user=User.objects.get(username='student_1'))


def force_login_teacher(instance):
    instance.client.force_login(user=User.objects.get(username='teacher_1'))


class CourseModelTest(TestCase):
    def test_string_representation(self):
        course = create_example_course()
        self.assertEqual(course.name, str(course))

    def test_creation_date(self):
        course = create_example_course()
        self.assertEqual(course.creation_date.minute, timezone.now().minute)

    def test_teachers_and_students(self):
        course = create_example_course()
        self.assertQuerysetEqual(
            course.students.all(),
            ('<User: student_1>', '<User: student_2>'),
            ordered=False
        )
        self.assertQuerysetEqual(
            course.teachers.all(),
            ('<User: teacher_1>', '<User: teacher_2>'),
            ordered=False
        )


class LessonModelTest(TestCase):
    def test_string_representation(self):
        lesson = create_example_lesson()
        self.assertEqual(lesson.title, str(lesson))

    def test_publication_and_modification_date(self):
        lesson = create_example_lesson()
        self.assertEqual(
            lesson.publication_date.minute, timezone.now().minute
        )
        self.assertEqual(
            lesson.modification_date.minute, timezone.now().minute
        )


class QuestionModelTest(TestCase):
    def test_string_representation(self):
        question = create_example_question()
        self.assertEqual(str(question), '{} – {}'.format(
            question.lesson.title, question.id))

    def test_ask_and_answer_date(self):
        question = create_example_question()
        self.assertEqual(
            question.ask_date.minute, timezone.now().minute
        )
        self.assertIsNone(question.answer_date)

    def test_default_answer_text_and_date(self):
        question = create_example_question()
        self.assertEqual(question.answer_text, '')
        self.assertIsNone(question.answer_date)


class LessonListViewTest(TestCase):
    def test_ok_response(self):
        create_example_lesson()
        force_login_student(self)
        response = self.client.get(reverse('moodle:lesson_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_contains_lesson_name(self):
        lesson = create_example_lesson()
        force_login_student(self)
        response = self.client.get(reverse('moodle:lesson_list'))
        self.assertIn(lesson.title, str(response.content))


class LessonDetailViewTest(TestCase):
    def test_ok_response(self):
        lesson = create_example_lesson()
        force_login_student(self)
        response = self.client.get(
            reverse('moodle:lesson_view', kwargs={'pk': lesson.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_contains_lesson_title_and_text(self):
        lesson = create_example_lesson()
        force_login_student(self)
        response = self.client.get(
            reverse('moodle:lesson_view', kwargs={'pk': lesson.pk}))
        self.assertIn(lesson.title, str(response.content))
        self.assertIn(lesson.text, str(response.content))

    def test_question_post(self):
        question = create_example_question()
        force_login_teacher(self)
        response = self.client.post(
            reverse('moodle:lesson_view',
                    kwargs={'pk': question.lesson.pk}),
            data={'text': 'A question.'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)


class LessonAddFormViewTest(TestCase):
    def test_get(self):
        question = create_example_question()
        force_login_teacher(self)
        response = self.client.get(reverse('moodle:lesson_add'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        question = create_example_question()
        force_login_teacher(self)
        response = self.client.post(
            reverse('moodle:lesson_add'),
            data={'course': question.lesson.course.id,
                  'title': 'Lesson about thing.',
                  'text': 'A good lesson.'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)


class CourseListViewTest(TestCase):
    def test_ok_response(self):
        create_example_course()
        force_login_student(self)
        response = self.client.get(reverse('moodle:course_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_contains_lesson_title(self):
        course = create_example_course()
        force_login_student(self)
        response = self.client.get(reverse('moodle:course_list'))
        self.assertIn(course.name, str(response.content))


class CourseDetailViewTest(TestCase):
    def test_ok_response(self):
        lesson = create_example_lesson()
        force_login_student(self)
        response = self.client.get(
            reverse('moodle:course_view', kwargs={'pk': lesson.course.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_contains_course_title(self):
        lesson = create_example_lesson()
        force_login_student(self)
        response = self.client.get(
            reverse('moodle:course_view', kwargs={'pk': lesson.course.pk}))
        self.assertIn(lesson.title, str(response.content))


class QuestionAnswerFormViewTest(TestCase):
    def test_get(self):
        question = create_example_question()
        force_login_teacher(self)
        response = self.client.get(
            reverse('moodle:question_answer_form',
                    kwargs={'lesson_pk': question.lesson.pk,
                            'question_pk': question.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        question = create_example_question()
        force_login_teacher(self)
        response = self.client.post(
            reverse('moodle:question_answer_form',
                    kwargs={'lesson_pk': question.lesson.pk,
                            'question_pk': question.pk}),
            data={'answer_text': 'Answer.'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)


class ViewAccessTest(TestCase):
    def test_login_redirect_when_not_authenticated(self):
        create_example_question()
        for url in ('moodle:index', 'moodle:lesson_list',
                    'moodle:course_list'):
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 302)
            self.assertIn('login', response.url)

    def test_access_denied_when_not_authenticated(self):
        question = create_example_question()
        urls_args = (
            (
                'moodle:lesson_view',
                {'pk': question.lesson.pk}
            ),
            (
                'moodle:lesson_add',
                None
            ),
            (
                'moodle:course_view',
                {'pk': question.lesson.course.pk}
            ),
            (
                'moodle:question_answer_form',
                {'lesson_pk': question.lesson.pk, 'question_pk': question.pk}
            )
        )
        for url, kwargs in urls_args:
            response = self.client.get(reverse(url, kwargs=kwargs))
            self.assertIn('Access to this part of the website '
                          'is currently not possible', str(response.content))
