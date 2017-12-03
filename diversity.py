import random
import sys
import csv
import os

# 제작 : 남도현(LegenDUST)
# 제작 이유 : 생명과학 숙제의 실험용. 환경의 변화가 급격할수록 유전적 다양성이 높은 집단이 생존에 더 유리하다는 것을 실험으로써 알아본다.
# 입력 값 : 환경의 변화율
# 출력 값 : 그 환경에서의 실험을 10번을 반복한 데이터.(csv 포맷)


class Gene:
    def __init__(self, number=-1):
        if number == -1:
            self.number = random.randrange(0, 101)
        else:
            self.number = number

    def mutate(self, rate):
        return Gene(int(round(self.number + random.gauss(0, rate))))


class Creature:
    def __init__(self, gene=None):
        if gene is None:
            self.gene = Gene()
        else:
            self.gene = gene
        self.death = False

    def reproduce(self, rate):
        nextgen1 = Creature(self.gene.mutate(rate))
        nextgen2 = Creature(self.gene.mutate(rate))
        return nextgen1, nextgen2

    def kill(self):
        self.death = True

    def __str__(self):
        return str(self.death)


class Species:
    def __init__(self, mutate_rate):
        self.creature_list = []
        for a in range(100):
            self.creature_list.append(Creature())
        self.mutate_rate = mutate_rate

    def get_size(self):
        return len(self.creature_list)

    def __str__(self):
        return str(len(self.creature_list))

    def next_gen(self):
        next_list = []
        for next_creature in self.creature_list:
            next_list += next_creature.reproduce(self.mutate_rate)
        self.creature_list = next_list

    def process_kill(self):
        next_list = []
        for next_creature in self.creature_list:
            if not next_creature.death:
                next_list.append(next_creature)
        self.creature_list = next_list

    def to_csv(self):
        return_list = []
        for next_creature in self.creature_list:
            return_list.append(str(next_creature.gene.number))
        return return_list


class Environment:
    def __init__(self, env_change_rate):
        self.species_list = [Species(0.1),
                             Species(0.4),
                             Species(1),
                             Species(3),
                             Species(5)]
        self.env_change_rate = env_change_rate
        self.env_num = random.randrange(0, 101)
        self.generation = 0

    def change_env(self):
        random_val = random.gauss(0, self.env_change_rate)
        if self.env_num + random_val > 100 or self.env_num + random_val < 0:
            next_num = self.env_num - random_val
        else:
            next_num = self.env_num + random_val
        self.env_num = round(next_num)

    def is_dead(self, creature):
        num = creature.gene.number
        if -10 < num - self.env_num < 10:
            if random.random() < 0.9:
                return False
            else:
                return True
        elif -20 < num - self.env_num < 20:
            if random.random() < 0.8:
                return False
            else:
                return True
        elif -30 < num - self.env_num < 30:
            if random.random() < 0.1:
                return False
            else:
                return True
        else:
            if random.random() < 0.01:
                return False
            else:
                return True

    def natural_selection(self):
        for next_species in self.species_list:
            for next_creature in next_species.creature_list:
                if self.is_dead(next_creature):
                    next_creature.kill()

        for next_species in self.species_list:
                next_species.process_kill()

        for next_species in self.species_list:
            next_species.next_gen()

        creature_num = 0
        for next_species in self.species_list:
            creature_num += next_species.get_size()

        if creature_num > 500:
            to_kill = creature_num - 500
            kill_list = random.sample(range(1, creature_num + 1), to_kill)
            counter = 1
            for next_species in self.species_list:
                for next_creature in next_species.creature_list:
                    if counter in kill_list:
                        next_creature.kill()
                    counter += 1

            for next_species in self.species_list:
                next_species.process_kill()

        self.generation += 1

    def __str__(self):
        return "현재 환경 : " + str(self.env_num) + ", 현재 환경 변화도 : " + \
               str(self.env_change_rate) + ", 현재 세대 : " + str(self.generation) +\
               "\n집단 1(0.1) : " + str(self.species_list[0]) + ", 집단2(0.4) : " + \
               str(self.species_list[1]) + ", 집단 3(1) : " + str(self.species_list[2]) + \
               ", 집단 4(3) : " + str(self.species_list[3]) + \
               ", 집단 5(5) : " + str(self.species_list[4]) + "\n\n"

    def to_csv(self):
        return [self.generation, self.species_list[0].get_size(), self.species_list[1].get_size(),
                self.species_list[2].get_size(), self.species_list[3].get_size(), self.species_list[4].get_size()]

    def print_species_to_csv(self):
        counter = 1
        for species in self.species_list:
            with open(str(counter) + ".csv", "a", encoding='utf-16', newline='') as file:
                species_writer = csv.writer(file)
                species_writer.writerow(species.to_csv())
            counter += 1

    def get_result(self):
        return [self.species_list[0].get_size(), self.species_list[1].get_size(),
                self.species_list[2].get_size(), self.species_list[3].get_size(), self.species_list[4].get_size()]


if len(sys.argv) != 2:
    print("input environment change rate")
else:
    if not os.path.isdir("./" + sys.argv[1] + "/"):
        os.mkdir("./" + sys.argv[1] + "/")
    with open("./" + sys.argv[1] + "/output of " + sys.argv[1] + ".csv", 'w', encoding='utf-16', newline='') as f:
        for j in range(10):
            wr = csv.writer(f)
            env = Environment(float(sys.argv[1]))
            print(env)
            for i in range(100):
                env.change_env()
                env.natural_selection()
                print(env)
            wr.writerow(env.get_result())
