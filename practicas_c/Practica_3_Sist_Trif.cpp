#include<iostream>
#include<math.h>
#define PI 3.14159265
using namespace std;

float convParteReal(float angulo, float magnitud){
    return magnitud * cos(angulo * PI / 180.0);
}

float convParteImaginaria(float angulo, float magnitud){
    return magnitud * sin(angulo * PI / 180.0);
}

float magnitudPolar(float cReal, float cImag){
    float res;
    res= sqrt(pow(cReal,2)+pow(cImag,2));
    return res;
}
float anguloPolar(float cReal, float cImag){
    float res;
    res=atan2(cImag,cReal)*180/PI;
    return res;
}
using namespace std;
int main(){
    int typ, ord;
    float vL, vF[3], zM, zA, IM[3], IA[3], Ireal[3],Imagi[3], a[3],cReal[3],cImag[3];
    cout<<"Ingrese el voltaje de línea del sistema trifásico:"<<endl;
    cin>>vL;
    cout<<"Ingrese la magnitud de la impedancia:"<<endl;
    cin>>zM;
    cout<<"Ingrese el ángulo de la impedancia:"<<endl;
    cin>>zA;
    cout<<"El sistema está dado en:"<<endl<<"1.- Delta"<<endl<<"2.- Estrella"<<endl;
    cin>>typ;
    cout<<"El orden es:"<<endl<<"1.- ABC"<<endl<<"2.- ACB"<<endl;
    cin>>ord;
    switch(typ){
        case 1:
            if(ord==1){
                a[1]=120;
                a[2]=0;
                a[3]=240;
            }
            if(ord==2){
                a[1]=240;
                a[2]=0;
                a[3]=120;
            }
            for(int i=1;i<=3;i++){
                vF[i]=vL/zM;
                IA[i]=a[i]-zA;
                cReal[i]= convParteReal(IA[i], vF[i]);
                cImag[i]= convParteImaginaria(IA[i], vF[i]);
            }
            Ireal[1]=cReal[1]-cReal[3];
            Imagi[1]=cImag[1]-cImag[3];
            Ireal[2]=cReal[2]-cReal[1];
            Imagi[2]=cImag[2]-cImag[1];
            Ireal[3]=cReal[3]-cReal[2];
            Imagi[3]=cImag[3]-cImag[2];
            
            for(int i=1;i<=3;i++){
                IM[i]=magnitudPolar(cReal[i], cImag[i]);
                IA[i]=anguloPolar(cReal[i], cImag[i]);
                cout<<"I"<<i<<" = "<<IM[i]<<"  "<<IA[i]<<endl;
            }
        break;
        case 2:
            if(ord==1){
                a[1]=90;
                a[2]=-30;
                a[3]=-150;
            }
            if(ord==2){
                a[1]=-90;
                a[2]=30;
                a[3]=150;
            }
            for(int i=1;i<=3;i++){
                vF[i]=(vL/sqrt(3))/zM;
                cout<<"operacion de angulos: "<<a[i]<<"-"<<zA<<endl;
                IA[i]=a[i]-zA;
                cout<<"I"<<i<<" = "<<vF[i]<<"  "<<IA[i]<<endl;
            }
        break;
    }
}