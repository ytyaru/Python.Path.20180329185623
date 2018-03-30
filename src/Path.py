import os, os.path, pathlib

class Path:
    def __init__(self, root='/', child='', is_expand=False):
        self.Root = root
        self.Child = child
        self.IsExpand = is_expand

    def __getitem__(self, key):
        if type(key) == int:
            split = self.Expand(self.FullPath).lstrip(os.sep).split(os.sep)
            return split[key]
        if type(key) == str:
            if 'Extension' == key or 'ext' == key: return self.GetExtension(self.FullPath)
            elif 'FileName' == key or 'basename' == key: return self.GetFileName(self.FullPath)
            elif 'FileNameWithoutExtension' == key or 'stem' == key: return self.GetFileNameWithoutExtension(self.FullPath)
            elif 'DirectoryName' == key or 'dirname' == key: return self.GetDirectoryName(self.FullPath)

    # this + ?, this / ?  連結する
    def __add__(self, other):
        return Path(self.Join(str(other).strip(os.sep)))
    def __truediv__(self, other): return self.__add__(other)

    # ? + this, ? / this  連結する
    def __radd__(self, other): return self.__add__(other)
    def __rtruediv__(self, other): return self.__add__(other)
        
    # += /= 連結する
    def __iadd__(self, other):
        self.Root = self.Join(self.Root, str(self.__add__(str(other).strip(os.sep))))
        return self
    def __itruediv__(self, other): return self.__iadd__(other)
       
    # ~ 展開する
    def __invert__(self): return self.Expand(self.FullPath)
    
    def __str__(self): return self.FullPath

    @property
    def Root(self): return self.__root
    @Root.setter
    def Root(self, v):
        if os.path.isabs(os.path.expandvars(os.path.expanduser(v))): self.__root = str(v)
        else: raise ValueError('Rootの値には絶対パスを指定してください。値={}'.format(v))

    @property
    def Child(self): return self.__child
    @Child.setter
    def Child(self, v):
        if not os.path.isabs(os.path.expandvars(os.path.expanduser(v))): self.__child= str(v)
        else: raise ValueError('Childの値にはRootからの相対パスを指定してください。値={}'.format(v))

    @property
    def IsExpand(self): return self.__is_expand
    @IsExpand.setter
    def IsExpand(self, v):
        if isinstance(v, bool): self.__is_expand = v
        else: raise TypeError('IsExpandの値にはbool型の値を渡してください。型={}, 値={}'.format(type(v), v))

    @property
    def FullPath(self):
        if self.Child is not None and 0 < len(self.Child):
            p = os.path.join(self.Root, self.Child)
        else: p = self.Root
        return self.Expand(p) if self.IsExpand else p

    def Join(self, *child_parts):
        if child_parts is None or 0 == len(child_parts): p = os.path.join(self.Root, self.Child)
        else: p = os.path.join(self.Root, self.__ListToStr(child_parts))
        return self.Expand(p) if self.IsExpand else p

    def FullPaths(self, *children):
        if type(children[0]) == list:
            target = children[0]
        else:
            target = children
        return [self.Expand(os.path.join(self.Root, child)) if self.IsExpand else os.path.join(self.Root, child) for child in target]
    
    # IN :['/A', ['B','C'], [['D',['E']]]]
    # OUT:/A/B/C/D/E
    @classmethod
    def __ListToStr(cls, target):
        if type(target) == list or type(target) == tuple:
            parts = []
            for t in target:
                if type(t) == str: parts.append(t)
                elif isinstance(t, os.PathLike): parts.append(str(t))
                elif type(t) == list or type(t) == tuple:
                    parts.append(cls.__ListToStr(t))
                else: raise TypeError('パスにはstr,os.PathLikeか、それらを含んだlist,tupleを使用してください。type={}'.format(type(t)))
            return os.path.join(*parts)
        return target
    
    @classmethod
    def ChangeExtension(cls, path, extension:str):
        base, ext = os.path.splitext(path)
        if 0 == len(ext): raise ValueError('指定されたパスは拡張子を含んでいません。path={}'.format(path))
        return base + '.' + extension
         
    @classmethod
    def Combine(cls, *args): return cls.__ListToStr(args)

    @classmethod
    def GetDirectoryName(cls, path): return os.path.dirname(path)

    @classmethod
    def GetExtension(cls, path): return os.path.splitext(path)[1]

    @classmethod
    def GetFileName(cls, path): return os.path.basename(path)

    @classmethod
    def GetFileNameWithoutExtension(cls, path): return cls.GetFileName(path).replace(cls.GetExtension(path), '')

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
