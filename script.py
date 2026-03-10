from random import choice

from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Subject
from datacenter.models import Teacher


def fix_marks(schoolkid: Schoolkid) -> None:
    """Corrects the bad grades of a given schoolkid."""
    qs_bad_points_child = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for bad_point in qs_bad_points_child:
        bad_point.points = 5
        bad_point.save()


def remove_chastisements(schoolkid: Schoolkid) -> None:
    """Deletes the chastisements of a given schoolkid. """
    qs_chastisements_child = Chastisement.objects.filter(schoolkid=schoolkid)
    for chast in qs_chastisements_child:
        chast.delete()


def create_commendation(schoolkid: Schoolkid, subject: Subject):
    """Creates commendation for a given student in a lesson on a given subject."""
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
    ]
    qs_lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        )
    qs_lessons_by_subject = qs_lessons.filter(subject=subject)
    first_lesson = choice(qs_lessons_by_subject)
    teacher = Teacher.objects.get(full_name=first_lesson.teacher)

    new_commendation = Commendation.objects.create(
        text=choice(commendations),
        created=first_lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher,
        )
    

def get_schoolkid_by_filter(schoolkid_filter: str) -> Schoolkid:
    """Returns the schoolkid by the filter"""
    return Schoolkid.objects.filter(full_name__contains=schoolkid_filter).get()


def get_schoolkid_subject_by_filter(schoolkid: Schoolkid, subject_filter: str) -> Subject:
    """Returns the subject by schoolkid and filter"""
    return Subject.objects.filter(
                title=subject_filter,
                year_of_study=schoolkid.year_of_study
                ).get()


def main(schoolkid_input: str, subject_input: str = None):
    try:
        schoolkid = get_schoolkid_by_filter(schoolkid_input)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено более одного ученика. Уточните свой запрос.')
        return
    except Schoolkid.DoesNotExist:
        print(f'По запросу "{schoolkid_input}" не найдено совпадений.')
        return

    if schoolkid and subject_input:
        try:
            subject = get_schoolkid_subject_by_filter(schoolkid, subject_input)
            create_commendation(schoolkid, subject)
        except Subject.MultipleObjectsReturned:
            print('Найдено более одного предмета. Уточните свой запрос.')
            return
        except Subject.DoesNotExist:
            print(f'По запросу "Ученик: {schoolkid_input} | Предмет: {subject_input}" '
                  f'не найдено совпадений.')
            return