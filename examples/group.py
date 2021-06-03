'''Example argument group.'''
from argufy import Parser

# parser = argparse.ArgumentParser()
parser = Parser()

group1 = parser.add_argument_group('group1')
group2 = parser.add_argument_group('group2')

group1.add_argument('test-g1')
group1.add_argument('--option1')

group2.add_argument('test-g2')
group2.add_argument('--option2')

print(parser.parse_known_args())
# parser.dispatch()
