from abc import ABC, abstractmethod
from enum import Enum


class ClassType(Enum):
    WARRIOR = "warrior"
    MAGE    = "mage"
    HEALER  = "healer"


# ─────────────────────────────  АБСТРАКЦИЯ  ─────────────────────────────

class Player(ABC):
    """Базовый контракт: любой игрок умеет атаковать, получать урон и лечиться."""

    def __init__(self, name, level, class_type, health=30, inventory=None):
        self.name = name
        self.level = level
        self.class_type = class_type
        self.max_health = health
        self.__health = health
        self.inventory = inventory if inventory is not None else []

    # --- инкапсуляция: здоровье меняется только через методы ---
    @property
    def health(self):
        return self.__health

    @property
    def alive(self):
        return self.__health > 0

    # --- абстракция: каждый класс персонажа атакует по-своему ---
    @abstractmethod
    def attack(self, target):
        """Обязан реализовать каждый наследник."""

    # --- общее поведение: наследуется или переопределяется ---
    def take_damage(self, damage):
        self.__health = max(0, self.__health - damage)
        print(f"  {self.name} получает {damage} урона → {self.__health}/{self.max_health}")
        if not self.alive:
            print(f"  💀 {self.name} повержен!")

    def heal(self, amount):
        before = self.__health
        self.__health = min(self.max_health, self.__health + amount)
        print(f"  {self.name} восстановил {self.__health - before} HP → {self.__health}/{self.max_health}")

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"  {self.name} положил в инвентарь: {item}")

    def __str__(self):
        return f"{type(self).__name__}({self.name}, lvl {self.level}, hp {self.__health}/{self.max_health})"


# ─────────────────────────────  ПОЛИМОРФИЗМ  ────────────────────────────

class Warrior(Player):
    def __init__(self, name, level, inventory=None):
        super().__init__(name, level, ClassType.WARRIOR, health=50, inventory=inventory)
        self.armor = 5

    def attack(self, target):
        print(f"{self.name} рубит мечом!")
        target.take_damage(self.level * 4)

    def take_damage(self, damage):
        blocked = min(self.armor, damage)
        if blocked:
            print(f"  {self.name} блокирует {blocked} урона бронёй")
        super().take_damage(damage - blocked)


class Mage(Player):
    def __init__(self, name, level, inventory=None):
        super().__init__(name, level, ClassType.MAGE, health=20, inventory=inventory)
        self.mana = 50

    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            print(f"{self.name} кастует огненный шар (мана: {self.mana})")
            target.take_damage(self.level * 10)
        else:
            print(f"{self.name} без маны — бьёт посохом")
            target.take_damage(2)

    def take_damage(self, damage):
        boosted = int(damage * 1.25)                 # маги хрупкие
        print(f"  {self.name} хрупкий — урон усилен до {boosted}")
        super().take_damage(boosted)


class Healer(Player):
    def __init__(self, name, level, inventory=None):
        super().__init__(name, level, ClassType.HEALER, health=30, inventory=inventory)

    def attack(self, target):
        print(f"{self.name} бьёт посохом")
        target.take_damage(self.level * 3)

    def heal(self, amount):
        super().heal(amount * 2)                     # самоисцеление x2

    def heal_ally(self, ally):
        amount = self.level * 5
        print(f"{self.name} направляет исцеление на {ally.name}")
        ally.heal(amount)

# 1. Абстракция в действии — Player создать нельзя
try:
    Player("Ghost", 1, ClassType.WARRIOR)
except TypeError as e:
    print(f"Абстракцию не инстанцировать → TypeError: {e}")
print()


# 2. Отряд — разные подклассы в одном списке
party = [
    Warrior("Conan", 3),
    Mage("Merlin", 2),
    Healer("Terri", 2),
]
for p in party:
    print(f"  {p}")
print()


# 3. Полиморфная атака: один вызов — три поведения
print("=== Атаки ===")
for i, fighter in enumerate(party):
    target = party[(i + 1) % len(party)]
    fighter.attack(target)
    print()


# 4. Полиморфный урон: броня / хрупкость / базовый
print("=== Получаем урон ===")
for p in party:
    p.take_damage(5)
    print()


# 5. Хилер лечит отряд (isinstance + полиморфизм heal)
print("=== Лечение ===")
for healer in (p for p in party if isinstance(p, Healer)):
    for ally in party:
        if ally is not healer and ally.alive:
            healer.heal_ally(ally)
print()


# 6. Итог
print("=== Состояние отряда ===")
for p in party:
    status = "жив" if p.alive else "мёртв"
    print(f"  {p}  [{status}]")






