from dataclasses import dataclass
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_ENERGY_CAL_A: float = 18
    RUN_ENERGY_CAL_B: float = 20
    M_IN_KM: float = 1000

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.RUN_ENERGY_CAL_A * self.get_mean_speed()
                - self.RUN_ENERGY_CAL_B) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_MASS_COEFF_A: float = 0.035
    WLK_MASS_COEFF_B: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.WLK_MASS_COEFF_A * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.WLK_MASS_COEFF_B * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWM_SPEED_COEFF: float = 1.1
    SWM_MASS_COEFF: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_SPEED_COEFF)
                * self.SWM_MASS_COEFF * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    sport_map: Dict[str, str] = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking}
    return sport_map.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: str = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
