from meetings.game import Game


def test(scenario_id, p0_id, p1_id):
    history_id = Game.create(scenario_id, p0_id, p1_id)

    counter = 0

    while part := Game.get_last_part(history_id):
        print(f'#{counter} {part["question"]["file_id"]}')
        for i, answer in enumerate(part['answers']):
            print(f'[{i}] {answer["file_id"]}')
        answer = input()
        Game.add_answer(answer, history_id, counter)
        counter += 1


def main():
    test(1, 1, 2)


if __name__ == '__main__':
    main()
