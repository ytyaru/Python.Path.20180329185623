import os, os.path, pathlib

class Path:
    def __init__(self, root='/', child='', is_expand=False):
        #self.__is_expand = is_expand
        #self.__root = root_path
        #if not os.path.isabs(path): raise Exception('root_pathが絶対パスではありません。root_path={}'.format(self.__root))
        self.Root = root
        self.Child = child
        self.IsExpand = is_expand

    @property
    def Root(self): return self.__root
    @Root.setter
    def Root(self, v):
        if isinstance(v, str):
            if os.path.isabs(v): self.__root = v
            else: raise Exception('Rootの値には絶対パスを指定してください。')
        elif isinstance(v, os.PathLike):
            if v.is_absolute(): self.__root = str(v)
            else: raise Exception('Rootの値には絶対パスを指定してください。')
    @property
    def Child(self): return self.__child
    @Child.setter
    def Child(self, v):
        if not os.path.isabs(v): self.__child = v
        else: raise Exception('Childの値にはRootからの相対パスを指定してください。')
    @property
    def IsExpand(self): return self.__is_expand
    @IsExpand.setter
    def IsExpand(self, v):
        if isinstance(v, bool): self.__is_expand = v
        else: raise Exception('IsExpandの値にはbool型の値を渡してください。')
    @property
    def FullPath(self):
        p = os.path.join(self.Root, self.Child)
        return self.Expand(p) if self.IsExpand else p
    def Join(self, *child_parts):
        if child_parts is None or 0 == len(child_parts): p = os.path.join(self.Root, self.Child)
        else:
            p = os.path.join(self.Root, self.__ListToStr(child_parts))
            #child = ''
            #for part in child_parts:
            #    if isinstance(part, str): child = os.path.join(child, part)
            #    elif isinstance(part, os.PathLike): child = os.path.join(child, str(part))
            #    elif isinstance(part, list): child = os.path.join(child, os.path.join(*[str(p) for p in part]))
            #    else: raise Exception('child_partsはstr, list<str>のいずれかにしてください。')
            #    #else: child += str(part)
            #p = os.path.join(self.Root, child)
        return self.Expand(p) if self.IsExpand else p
        #parts = [str(c) for c in child_parts]
        #if child_parts is None: p = os.path.join(self.Root, self.Child)
        #else: p = os.path.join(self.Root, *[str(c) for c in child_parts])
        #return self.Expand(p) if self.IsExpand else p
    def FullPaths(self, *children):
        if type(children[0]) == list:
            return [os.path.join(self.Root, child) for child in children[0]]
        else:
            return [os.path.join(self.Root, child) for child in children]
        #return [os.path.join(self.Root, child) for child in self.__ListToStr(children)]
        #return [os.path.join(self.Root, str(child)) for child in children]
    #def FullPaths(self, *children): return [os.path.join(self.Root, str(child)) for child in children]

    # IN :['/A', ['B','C'], [['D',['E']]]]
    # OUT:/A/B/C/D/E
    def __ListToStr(self, target):
        if type(target) == list or type(target) == tuple:
            parts = []
            for t in target:
                if type(t) == str: parts.append(t)
                elif isinstance(t, os.PathLike): parts.append(str(t))
                #elif type(t) == os.PathLike: parts.append(str(t))
                #elif type(t) == list or type(t) == tuple: return self.__ListToStr(t)
                elif type(t) == list or type(t) == tuple:
                    parts.append(self.__ListToStr(t))
                    #parts.append(self.__ListToStr(t))
                else: raise Exception('パスにはstr,os.PathLikeか、それらを含んだlist,tupleを使用してください。type={}'.format(type(t)))
            #print('*', parts, os.path.join(*parts))
            #for i, p in enumerate(parts):
            #    if type(parts[i]) == list or type(parts[i]) == tuple:
            #        parts[i]
            return os.path.join(*parts)
        return target

        #if isinstance(target, list):
        #    parts = []
        #    for t in target:
        #        if isinstance(t, str): parts.append(t)
        #        if isinstance(t, bytes): parts.append(t)
        #        elif isinstance(t, os.PathLike): parts.append(str(t))
        #        elif isinstance(t, list): parts.append(__ListToStr(t))
        #    return os.path.join(*parts)
        #

        #if isinstance(target, list):
        #    children = []
        #    for item in target:
        #        children.append(self.__ListToStr(item))
        #    return os.path.join(*children)
        #else: return str(target)


    @classmethod
    def ChangeExtension(cls, path, extension:str):
        base, ext = os.path.splitext(path)
        if 0 == len(ext): raise Exception('指定されたパスは拡張子を含んでいません。')
        return base + '.' + extension
         
    @classmethod
    def Combine(cls, *args): return os.path.join(*[str(a) for a in args])

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
