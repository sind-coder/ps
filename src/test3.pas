function fact(int f; int i; int d){
while (i<f) {
d = d*i;
i = i+1
};
return d*f
}

int x, y, j, r

{
x=1;
y=5;
j=1;
while(x<y){
r=1;
r=fact(x, j, r);
write(r);
write(",");
x=x+1
}
}
