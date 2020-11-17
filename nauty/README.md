# Nauty 

### Instructions
```bash
cd nauty
chmod +x configure
./configure
make
``` 

### Executables
This custom code creates a number of additional executables.
1) ```gengpg``` and ```gengadj``` are identical  in function to ```geng```,  except  that  they output  graphs in pg and adjacency  matrix  formats, respectively.
2)  ```nautytopg``` takes as input graphs in graph6 format and outputs them in pg format.  This is useful if you want to run the output of geng through another nauty executable before converting it to pg format.
3)  ```pgtonauty``` takes as input graphs in pg format and outputs them in graph6 format.  This is useful if you want to convert the output of pg back to nauty format for some reason.
4)  ```twin```  takes  as  input  graphs  in  graph6  format  and  outputs  those  that  are  P-twins,  where  a  graph  G  is  a  P-twin  for  some property P if P holds for the  graph and its complement.  Typing 
```bash
./geng 8 | ./twin -t
```
will list all spanning tree twins with 8 vertices.  Type ```./twin -help``` for an exhaustive list of properties and output formats.

5)  ```dh``` takes as input graphs in graph6 format and outputs those that are distance hereditary.  Like ```twin```, ```dh``` can output graphs in a variety of output formats.
