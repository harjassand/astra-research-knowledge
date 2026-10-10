import ctypes as c
from pathlib import Path
l=c.CDLL('libarchive.so.13')
l.archive_read_new.restype=c.c_void_p
for f in ['archive_read_support_filter_all','archive_read_support_format_all','archive_read_free']:
 getattr(l,f).argtypes=[c.c_void_p]
l.archive_read_open_filename.argtypes=[c.c_void_p,c.c_char_p,c.c_size_t]
l.archive_read_next_header.argtypes=[c.c_void_p,c.POINTER(c.c_void_p)]
l.archive_entry_pathname.argtypes=[c.c_void_p];l.archive_entry_pathname.restype=c.c_char_p
l.archive_entry_size.argtypes=[c.c_void_p];l.archive_entry_size.restype=c.c_longlong
l.archive_read_data.argtypes=[c.c_void_p,c.c_void_p,c.c_size_t];l.archive_read_data.restype=c.c_ssize_t
l.archive_read_data_skip.argtypes=[c.c_void_p]
def read(src,dest=None):
 a=l.archive_read_new();l.archive_read_support_filter_all(a);l.archive_read_support_format_all(a)
 assert l.archive_read_open_filename(a,str(src).encode(),10240)==0
 h=c.c_void_p(); names=[];buf=c.create_string_buffer(1024*1024)
 while l.archive_read_next_header(a,c.byref(h))==0:
  n=l.archive_entry_pathname(h).decode();s=l.archive_entry_size(h);names.append((n,s));print(n,s)
  if dest and s:
   q=Path(dest)/n
   assert '..' not in q.parts
   q.parent.mkdir(parents=True,exist_ok=True)
   with q.open('wb') as f:
    while (t:=l.archive_read_data(a,buf,len(buf)))>0:f.write(buf.raw[:t])
  else:l.archive_read_data_skip(a)
 l.archive_read_free(a);return names
if __name__=='__main__':
 import sys,json
 print(json.dumps(read(*sys.argv[1:]),indent=2))
