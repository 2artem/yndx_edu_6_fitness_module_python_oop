"""Программный модуль для фитренс-трекера, который:
принимает от блока датчиков информацию о прошедшей тренировке;
определяет вид тренировки, рассчитывает результаты тренировки;
выводит информационное сообщение о результатах тренировки.
"""


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Метод возвращает строку сообщения."""
        out_message = (f'Тип тренировки: {self.training_type}; '
                       f'Длительность: {self.duration:.3f} ч.; '
                       f'Дистанция: {self.distance:.3f} км; '
                       f'Ср. скорость: {self.speed:.3f} км/ч; '
                       f'Потрачено ккал: {self.calories:.3f}.'
                       )
        return out_message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_PER_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        calc_training_info_object = InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories())
        return calc_training_info_object


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        spent_calories = (
            (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
            * self.weight / self.M_IN_KM
            * (self.duration * self.MINUTES_PER_HOUR)
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        coeff_calorie_3 = 2
        spent_calories = ((coeff_calorie_1 * self.weight
                          + (self.get_mean_speed()**coeff_calorie_3
                           // self.height) * coeff_calorie_2 * self.weight)
                          * (self.duration * self.MINUTES_PER_HOUR))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        spent_calories = ((Swimming.get_mean_speed(self) + coeff_calorie_1)
                          * coeff_calorie_2 * self.weight
                          )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    # Коды тренировок полученные от датчиков и
    # сопоставимые с ними классы типов тренировок.
    training_code = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking,
                     }
    # Возврат созданного объекта соответствующего типу тренировки,
    # с проверкой наличия класса тренировки для полученного параметра
    # workout_type от датчиков устройства
    try:
        return training_code[workout_type](*data)
    except KeyError:
        print(f'KeyError: «{workout_type}» - от датчиков устройства '
              'получен неизвестный код тренировки.'
              )


def main(training: Training) -> None:
    """Главная функция."""
    if isinstance(training, Training):
        info = Training.show_training_info(training)
        print(InfoMessage.get_message(info))


if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
