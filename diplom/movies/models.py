from django.db import models
from datetime import date
# Create your models here.


class Category(models.Model):
    """ Категории """
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'


class Genre(models.Model):
    '''Жанры'''

    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """Фильм"""
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Имя', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.SlugField('Обложка', max_length=1000)
    year = models.PositiveSmallIntegerField('Год', default=0)
    country = models.CharField('Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Режисср', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name="Актеры", related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text='Указывать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="Указывать сумму в долларах"
    )
    fees_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="Указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class MovieShots(models.Model):
    """Снимки из фильма"""
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    "Звезды рейтинга"
    value = models.PositiveSmallIntegerField('Значение', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'

class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField('Название', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'