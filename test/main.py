import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Path import Path

if __name__ == '__main__':
    print(Path.ChangeExtension('/tmp/a.txt', 'csv'))
    print(Path.ChangeExtension(pathlib.Path('/tmp/a.txt'), 'csv'))
    print(Path.Combine('A','B','C'))
    print(Path.Combine(pathlib.Path('A'),'B','C'))
    print(Path.GetDirectoryName('/tmp/work/a.txt'))
    print(Path.GetExtension('/tmp/work/a.txt'))
    print(Path.GetFileName('/tmp/work/a.txt'))
    print(Path.GetFileNameWithoutExtension('/tmp/work/a.txt'))
    print(Path.GetFullPath('work/a.txt'))
    print(Path.Expand('~/root/a.txt'))
    print(Path.Expand('${HOME}/root/a.txt'))
    print(Path.Expand('$HOME/root/a.txt'))
    print(Path.RelativeTo('a.txt'))
    print(Path.RelativeTo('/home/pi/dir/a.txt', start='/home/pi/'))

    p = Path()
    print(p.Root)
    print(p.Child)
    print(p.IsExpand)

    #p.Root = 'A'
    p.Root = '/A'
    print(p.Root)
    #p.Child = '/B'
    p.Child = 'B'
    print(p.Child)
    print(p.FullPath)
    print(p.Join('C'))
    print(p.Join('C','D','E'))
    print(p.Join(['C','D','E']))
    print(p.Join(['C'],['D','E']))
    print(p.Join(['C'],['D',['E']]))
    print(p.Join(['C'],['D',['E',['F']]]))
    print(p.Join(('C'),('D',('E',('F')))))
    print(p.Join(['C'],('D',('E',('F')))))
    print(p.FullPaths('C','E/F', 'GH'))
    print(p.FullPaths(['C','E/F', 'GH']))

    p.Root = pathlib.Path('/A')
    print(p.Root)
    p.Child = pathlib.Path('B')
    print(p.Child)
    print(p.FullPath)
    print(p.Join())
    print(p.Join('C'))
    print(p.Join(pathlib.Path('C')))
    print(p.Join('C', pathlib.Path('D'), ('E',), ['F']))
    print(p.Join(['C', pathlib.Path('D'), ('E',), ['F']]))
    print(p.Join(['C', pathlib.Path('D'), ('E',pathlib.Path('F')), [pathlib.Path('G'),'H']]))
