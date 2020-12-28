from argufy import Parser

# parser = argparse.ArgumentParser()
parser = Parser()

group1 = parser.add_argument_group('group 1')
group2 = parser.add_argument_group('group 2')

group1.add_argument('test')
group1.add_argument('--option1')
group2.add_argument('--option2')

print(parser.parse_args())
