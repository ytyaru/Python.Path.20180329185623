import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Path import Path
import unittest

class PathTest(unittest.TestCase):
    # ----------------------------
    # クラスメソッド
    # ----------------------------
    def test_ChangeExtension(self):
        self.assertEqual('/tmp/a.csv', Path.ChangeExtension('/tmp/a.txt', 'csv'))
    def test_ChangeExtension_MultiDot(self):
        self.assertEqual('/tmp/a.txt.csv', Path.ChangeExtension('/tmp/a.txt.abc', 'csv'))


    def test_ChangeExtension_NotHasExtension(self):
        path = '/tmp/a'
        with self.assertRaises(ValueError) as e:
            Path.ChangeExtension(path, 'csv')
        self.assertEqual('指定されたパスは拡張子を含んでいません。path={}'.format(path), e.exception.args[0])

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
        self.assertEqual('A/a.txt', Path.RelativeTo('/tmp/A/a.txt', '/tmp'))
        self.assertEqual('a.txt', Path.RelativeTo('/tmp/A/a.txt', '/tmp/A'))
        self.assertEqual('../A/a.txt', Path.RelativeTo('/tmp/A/a.txt', '/tmp/B'))
    # ----------------------------
    # インスタンスメソッド
    # ----------------------------
    def test_Root(self):
        p = Path()
        self.assertEqual('/', p.Root)

        v = '/tmp'
        p.Root = v
        self.assertEqual(v, p.Root)
        p.Root = pathlib.Path(v)
        self.assertEqual(v, p.Root)

        p = Path(v)
        self.assertEqual(v, p.Root)
        p = Path(root=v)
        self.assertEqual(v, p.Root)

    def test_Root_NotAbsolute(self):
        v = 'A'
        p = Path()
        with self.assertRaises(ValueError) as e:
            p.Root = v
        self.assertEqual('Rootの値には絶対パスを指定してください。値={}'.format(v), e.exception.args[0])

        v = 'B'
        with self.assertRaises(ValueError) as e:
            p = Path(v)
        self.assertEqual('Rootの値には絶対パスを指定してください。値={}'.format(v), e.exception.args[0])

        v = 'C'
        with self.assertRaises(ValueError) as e:
            p = Path(root=v)
        self.assertEqual('Rootの値には絶対パスを指定してください。値={}'.format(v), e.exception.args[0])

    def test_Child(self):
        v = 'A'
        p = Path()
        self.assertEqual('', p.Child)
        p.Child= v
        self.assertEqual(v, p.Child)
        p.Child = pathlib.Path(v)
        self.assertEqual(v, p.Child)

        p = Path('/', v)
        self.assertEqual(v, p.Child)
        p = Path(child=v)
        self.assertEqual(v, p.Child)

    def test_Child_NotRelative(self):
        v = '/tmp'
        p = Path()
        with self.assertRaises(ValueError) as e:
            p.Child= v
        self.assertEqual('Childの値にはRootからの相対パスを指定してください。値={}'.format(v), e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            p = Path('/', v)
        self.assertEqual('Childの値にはRootからの相対パスを指定してください。値={}'.format(v), e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            p = Path(child=v)
        self.assertEqual('Childの値にはRootからの相対パスを指定してください。値={}'.format(v), e.exception.args[0])

    def test_IsExpand(self):
        p = Path()
        self.assertEqual(False, p.IsExpand)
        p.IsExpand = True
        self.assertEqual(True, p.IsExpand)

    def test_IsExpand_NotBool(self):
        v = 'TRUE'
        p = Path()
        with self.assertRaises(TypeError) as e:
            p.IsExpand = v
        self.assertEqual('IsExpandの値にはbool型の値を渡してください。型={}, 値={}'.format(type(v), v), e.exception.args[0])

        with self.assertRaises(TypeError) as e:
            p = Path(is_expand=v)
        self.assertEqual('IsExpandの値にはbool型の値を渡してください。型={}, 値={}'.format(type(v), v), e.exception.args[0])

    def test_Join(self):
        p = Path()
        self.assertEqual('/', p.Join())
        p = Path('/tmp', 'A')
        self.assertEqual('/tmp/B', p.Join('B'))
        p = Path('/tmp', 'A')
        self.assertEqual('/tmp/B/C.d', p.Join('B','C.d'))



    def test_FullPath(self):
        path = '~/A/b.c'
        p = Path(path)
        self.assertEqual('~/A/b.c', p.FullPath)
        p.IsExpand = True
        self.assertEqual(os.path.expanduser('~/A/b.c'), p.FullPath)
        p.IsExpand = False
        self.assertEqual('~/A/b.c', p.FullPath)

        root = '$HOME/A'
        child = 'b.c'
        p = Path(root, child)
        self.assertEqual('$HOME/A/b.c', p.FullPath)
        p = Path(root, child, True)
        self.assertEqual(os.path.expandvars('$HOME/A/b.c'), p.FullPath)

        root = '~/A'
        p = Path(root)
        self.assertEqual(root, p.FullPath)
        p = Path(root, is_expand=True)
        self.assertEqual(os.path.expanduser(root), p.FullPath)

    def test_FullPaths(self):
        root = '~/root'
        p = Path(root, is_expand=True)
        self.assertEqual([os.path.expanduser(os.path.join(root, 'A'))], p.FullPaths('A'))
        self.assertEqual([os.path.expanduser(os.path.join(root, 'A')), os.path.expanduser(os.path.join(root, 'B'))], p.FullPaths('A','B'))

        children = ['A', 'B']
        self.assertEqual([os.path.expanduser(os.path.join(root, c)) for c in children], p.FullPaths(children))

        self.assertEqual([os.path.expanduser(os.path.join(root, c)) for c in children], p.FullPaths(*children))

        children = [pathlib.Path('A'), pathlib.Path('B')]
        self.assertEqual([os.path.expanduser(os.path.join(root, c)) for c in children], p.FullPaths(children))

        self.assertEqual([os.path.expanduser(os.path.join(root, c)) for c in children], p.FullPaths(*children))

    def test_FullPaths_TypeError(self):
        p = Path()
        children = ['A', pathlib.Path('B'), ['C'], ('D',), [['E',['F']]]]
        with self.assertRaises(TypeError) as e:
            p.FullPaths(children)

    # ----------------------------
    # 演算子オーバーライド
    # ----------------------------

    def test_getitem_index(self):
        p = Path('/tmp', 'A/B/C.d')
        self.assertEqual('tmp', p[0])
        self.assertEqual('A', p[1])
        self.assertEqual('B', p[2])
        self.assertEqual('C.d', p[3])

        if os.name == 'posix':
            import getpass
            p = Path('~/root', 'A/B/C.d')
            self.assertEqual('home', p[0])
            self.assertEqual(getpass.getuser(), p[1])
            self.assertEqual('root', p[2])
            self.assertEqual('A', p[3])
            self.assertEqual('B', p[4])
            self.assertEqual('C.d', p[5])

    def test_getitem_OutOfIndex(self):
        p = Path('/tmp', 'C.d')
        with self.assertRaises(IndexError) as e:
            p[2]

    def test_getitem_name(self):
        p = Path('/tmp', 'A/B/C.d')
        self.assertEqual('.d', p['Extension'])
        self.assertEqual('.d', p['ext'])
        self.assertEqual('C.d', p['FileName'])
        self.assertEqual('C.d', p['basename'])
        self.assertEqual('C', p['FileNameWithoutExtension'])
        self.assertEqual('C', p['stem'])
        self.assertEqual('/tmp/A/B', p['DirectoryName'])
        self.assertEqual('/tmp/A/B', p['dirname'])
        self.assertEqual(None, p['NotExistKeyword'])

    def test_add(self):
        p = Path('/tmp', 'A/B')
        self.assertEqual('/tmp/C.d', str(p + 'C.d'))
        self.assertEqual('/tmp/C.d', str('C.d' + p))
        self.assertEqual('/tmp/C.d', str(p / 'C.d'))
        self.assertEqual('/tmp/C.d', str('C.d' / p))

        self.assertEqual('/tmp/C.d', str(p + '/C.d'))
        self.assertEqual('/tmp/C.d', str(p + 'C.d/'))
        self.assertEqual('/tmp/C.d', str(p + '/C.d/'))
        self.assertEqual('/tmp/C.d', str(p + '//C.d//'))

        self.assertEqual('/tmp/A', str(p + 'A'))
        self.assertEqual('/tmp/A/B', str(p + 'A' + 'B'))
        self.assertEqual('/tmp/A/B/C.d', str(p + 'A' + 'B' + '/C.d'))
        self.assertEqual('/tmp/A/B/C.d', str(p + 'A/B/C.d'))
        self.assertEqual('/tmp/A', str(p + pathlib.Path('A')))
        self.assertEqual('/tmp/A/B', str(p + 'A' + pathlib.Path('B')))
        self.assertEqual('/tmp/A/B', str(p + pathlib.Path('A') + 'B'))
        self.assertEqual('/tmp/A/B', str(p / 'A' / pathlib.Path('B')))
        self.assertEqual('/tmp/A/B', str(p / pathlib.Path('A') / 'B'))
        self.assertEqual('/tmp/A/B', str(p + pathlib.Path('A') / 'B'))
        self.assertEqual('/tmp/A/B', str(p / pathlib.Path('A') + 'B'))
        #self.assertEqual('/tmp/A/B/C', str('/tmp' + Path('A') / pathlib.Path('B') + 'C'))

    def test_iadd(self):
        p = Path()
        p += 'tmp'
        self.assertEqual('/tmp', str(p))
        p += 'A'
        self.assertEqual('/tmp/A', str(p))
        p /= 'B.c'
        self.assertEqual('/tmp/A/B.c', str(p))

        p = Path()
        p += 'tmp/work/'
        self.assertEqual('/tmp/work', str(p))
        p += '/A/'
        self.assertEqual('/tmp/work/A', str(p))
        p += 'B/C'
        self.assertEqual('/tmp/work/A/B/C', str(p))
        p += pathlib.Path('D')
        self.assertEqual('/tmp/work/A/B/C/D', str(p))
        #p += 'E' + pathlib.Path('F')
        #self.assertEqual('/tmp/work/A/B/C/D/E/F', str(p))

    def test_invert(self):
        p = Path('~/')
        self.assertEqual(os.path.expanduser('~/'), ~p)
        self.assertEqual(os.path.expandvars('$HOME'), ~Path('$HOME'))

    def test_len(self):
        p = Path()
        self.assertEqual(1, len(p))
        self.assertEqual(2, len(Path('/A/B')))
        self.assertEqual(4, len(Path('/A/B','C/D')))
        self.assertEqual(3, len(Path('/A/B','C/D')+'E'))

    def test_iter(self):
        expecteds = ['A','B','C']
        p = Path(os.sep + os.sep.join(expecteds))
        for i, item in enumerate(p):
            self.assertEqual(expecteds[i], p[i])

    def test_lshift(self):
        p = Path('/tmp/A/B/C')
        self.assertEqual('/tmp/A/B', p << 1)
        self.assertEqual('/tmp/A', p << 2)
        self.assertEqual('/tmp', p << 3)
        self.assertEqual('/', p << 4)

        self.assertEqual('/tmp/A/B/C', p << 0)
        self.assertEqual('/', p << -1)

    def test_parent(self):
        p = Path('/tmp/A/B/C')
        self.assertEqual('/tmp/A/B', str(p.Parent))
        self.assertEqual('/tmp/A', str(p.Parent.Parent))
        self.assertEqual('/tmp', str(p.Parent.Parent.Parent))
        self.assertEqual('/', str(p.Parent.Parent.Parent.Parent))
        self.assertEqual('/', str(p.Parent.Parent.Parent.Parent.Parent))


if __name__ == '__main__':
    unittest.main()
