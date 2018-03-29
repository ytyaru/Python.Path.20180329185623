import os, os.path, pathlib
import re
class Path:
    def __init__(self, base_path='/'):
        self.__base_path = base_path
        if not os.path.isabs(path): raise Exception('base_pathが絶対パスではありません。base_path={}'.format(self.__base_path))

    @classmethod
    def ChangeExtension(cls, path, extension:str):
        base, ext = os.path.splitext(path)
        if 0 == len(ext): raise Exception('指定されたパスは拡張子を含んでいません。')
        return base + '.' + extension
         
    @classmethod
    def Combine(cls, *args): return os.path.join(*[str(a) for a in args])
    #def Combine(cls, *args): return os.path.join(args)
    #def Combine(cls, *args): return os.sep.join([str(a) for a in args])
    #def Combine(cls, *args): return os.sep.join(args)

    @classmethod
    def GetDirectoryName(cls, path): return os.path.dirname(path)

    @classmethod
    def GetExtension(cls, path): return os.path.splitext(path)[1]

    @classmethod
    def GetFileName(cls, path): return os.path.basename(path)

    @classmethod
    def GetFileNameWithoutExtension(cls, path): return os.path.splitext(path)[0]

    @classmethod
    def GetFullPath(cls, path): return os.path.abspath(path)

    @classmethod
    def Expand(cls, path): return os.path.expandvars(os.path.expanduser(path))

    @classmethod
    def RelativeTo(cls, path, start=os.curdir): return os.path.relpath(path, start)

    __instance = None
    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


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

