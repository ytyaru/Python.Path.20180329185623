import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Path import Path
import unittest

class PathTest(unittest.TestCase):
    def test_ChangeExtension(self):
        self.assertEqual('/tmp/a.csv', Path.ChangeExtension('/tmp/a.txt', 'csv'))
    def test_ChangeExtension_MultiDot(self):
        self.assertEqual('/tmp/a.txt.csv', Path.ChangeExtension('/tmp/a.txt.abc', 'csv'))


    def test_ChangeExtension_NotHasExtension(self):
        with self.assertRaises(ValueError) as e:
            Path.ChangeExtension('/tmp/a', 'csv')
        self.assertEqual('指定されたパスは拡張子を含んでいません。', e.exception.args[0])

    def test_Combine_str_verlen(self):
        self.assertEqual('/tmp', Path.Combine('/tmp'))
        self.assertEqual('/tmp/A', Path.Combine('/tmp', 'A'))
        self.assertEqual('/tmp/A/B', Path.Combine('/tmp', 'A', 'B'))
        self.assertEqual('/tmp/A/B.txt', Path.Combine('/tmp', 'A', 'B.txt'))
        self.assertEqual('/tmp/A/B.txt/C', Path.Combine('/tmp', 'A', 'B.txt', 'C'))

    def test_Combine_str_list(self):
        self.assertEqual('/tmp', Path.Combine(['/tmp']))
        self.assertEqual('/tmp/A', Path.Combine(['/tmp', 'A']))
        self.assertEqual('/tmp/A/B', Path.Combine(['/tmp', 'A', 'B']))
        self.assertEqual('/tmp/A/B.txt', Path.Combine(['/tmp', 'A', 'B.txt']))
        self.assertEqual('/tmp/A/B.txt/C', Path.Combine(['/tmp', 'A', 'B.txt', 'C']))

    def test_Combine_str_tuple(self):
        self.assertEqual('/tmp', Path.Combine(('/tmp',)))
        self.assertEqual('/tmp/A', Path.Combine(('/tmp', 'A')))
        self.assertEqual('/tmp/A/B', Path.Combine(('/tmp', 'A', 'B')))
        self.assertEqual('/tmp/A/B.txt', Path.Combine(('/tmp', 'A', 'B.txt')))
        self.assertEqual('/tmp/A/B.txt/C', Path.Combine(('/tmp', 'A', 'B.txt', 'C')))

    def test_Combine_pathilb_Path_verlen(self):
        self.assertEqual('/tmp', Path.Combine(pathlib.Path('/tmp')))
        self.assertEqual('/tmp/A', Path.Combine(pathlib.Path('/tmp'), pathlib.Path('A')))
        self.assertEqual('/tmp/A/B', Path.Combine(pathlib.Path('/tmp'), pathlib.Path('A'), pathlib.Path('B')))
        self.assertEqual('/tmp/A/B.txt', Path.Combine(pathlib.Path('/tmp'), pathlib.Path('A'), pathlib.Path('B.txt')))
        self.assertEqual('/tmp/A/B.txt/C', Path.Combine(pathlib.Path('/tmp'), pathlib.Path('A'), pathlib.Path('B.txt'), pathlib.Path('C')))

    def test_Combine_type_mixture(self):
        self.assertEqual('/tmp/A', Path.Combine('/tmp', pathlib.Path('A')))
        self.assertEqual('/tmp/A', Path.Combine(pathlib.Path('/tmp'), 'A'))
        self.assertEqual('/tmp/A', Path.Combine(['/tmp'], (pathlib.Path('A'),)))
        self.assertEqual('/tmp/A/B', Path.Combine(['/tmp'], (pathlib.Path('A'),), 'B'))
        self.assertEqual('/tmp/A/B/C/D/E', Path.Combine(['/tmp', pathlib.Path('A')], (pathlib.Path('B'),'C'), 'D', pathlib.Path('E')))

    def test_GetDirectoryName(self):
        self.assertEqual('/tmp', Path.GetDirectoryName('/tmp/a.txt'))
        self.assertEqual('/tmp', Path.GetDirectoryName(pathlib.Path('/tmp/a.txt')))
        self.assertEqual('/tmp/A', Path.GetDirectoryName('/tmp/A/a.txt'))
        self.assertEqual('/tmp/A', Path.GetDirectoryName(pathlib.Path('/tmp/A/a.txt')))
        self.assertEqual('/tmp', Path.GetDirectoryName('/tmp/A'))
        self.assertEqual('/tmp', Path.GetDirectoryName(pathlib.Path('/tmp/A')))

    def test_GetExtension(self):
        self.assertEqual('.txt', Path.GetExtension('/tmp/a.txt'))
        self.assertEqual('.txt', Path.GetExtension('/tmp/a.csv.txt'))
        self.assertEqual('', Path.GetExtension('/tmp/.bashrc'))
        self.assertEqual('', Path.GetExtension('/tmp/A'))
  
    def test_GetFileName(self):
        self.assertEqual('a.txt', Path.GetFileName('/tmp/a.txt'))
        self.assertEqual('a.csv.txt', Path.GetFileName('/tmp/a.csv.txt'))
        self.assertEqual('.bashrc', Path.GetFileName('/tmp/.bashrc'))
        self.assertEqual('A', Path.GetFileName('/tmp/A'))
        self.assertEqual('', Path.GetFileName('/tmp/'))

    def test_GetFileNameWithoutExtensionGetFileName(self):
        self.assertEqual('a', Path.GetFileNameWithoutExtension('/tmp/a.txt'))
        self.assertEqual('x', Path.GetFileNameWithoutExtension('/tmp/Z/x.txt'))
        self.assertEqual('a.csv', Path.GetFileNameWithoutExtension('/tmp/a.csv.txt'))
        self.assertEqual('.bashrc', Path.GetFileNameWithoutExtension('/tmp/.bashrc'))
        self.assertEqual('A', Path.GetFileNameWithoutExtension('/tmp/A'))
        self.assertEqual('', Path.GetFileNameWithoutExtension('/tmp/'))
        
    def test_GetFullPath(self):
        root = os.path.normpath(os.getcwd())
        self.assertEqual(os.path.join(root, 'a.txt'), Path.GetFullPath('a.txt'))
        self.assertEqual(os.path.join(root, '/A/a.txt'), Path.GetFullPath('/A/a.txt'))
        self.assertEqual(os.path.abspath('../a.txt'), Path.GetFullPath('../a.txt'))

    def test_Expand(self):
        self.assertEqual(os.path.expanduser('~/'), Path.Expand('~/'))
        self.assertEqual(os.path.expanduser('~/A/B.c'), Path.Expand('~/A/B.c'))
        self.assertEqual(os.path.expandvars('$HOME/'), Path.Expand('$HOME/'))
        self.assertEqual(os.path.expandvars('$HOME/A/B.c'), Path.Expand('$HOME/A/B.c'))
        self.assertEqual(os.path.expandvars('${HOME}/A/B.c'), Path.Expand('${HOME}/A/B.c'))
        self.assertEqual(os.path.expandvars(os.path.expanduser('~/sub/${HOME}/A/B.c')), Path.Expand('~/sub/${HOME}/A/B.c'))
        
    def test_RelativeTo(self):
        self.assertEqual('a.txt', Path.RelativeTo('a.txt'))
        #self.assertEqual(os.path.join(os.path.expanduser('~/'), 'a.txt'), Path.RelativeTo('a.txt'))
        self.assertEqual('A/a.txt', Path.RelativeTo('/tmp/A/a.txt', '/tmp'))
        self.assertEqual('a.txt', Path.RelativeTo('/tmp/A/a.txt', '/tmp/A'))
        self.assertEqual('../A/a.txt', Path.RelativeTo('/tmp/A/a.txt', '/tmp/B'))

    def __GetPaths(self):
        return [['/tmp'], ['/tmp', 'A'], ['/tmp', 'A', 'B'], ['/tmp', 'A', 'B.txt']]


if __name__ == '__main__':
    unittest.main()
