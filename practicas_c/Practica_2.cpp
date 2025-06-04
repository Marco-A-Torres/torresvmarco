#include <iostream>
#include <string.h>

using namespace std;
int main(){
    int opc,cant;
    float n[10],res;
    cout<<"Ingrese la cantidad de numeros a operar (maximo 10)"<<endl;
    cin>>cant;
    for(int i=1;i<=cant;i++){
        cout<<"Ingrese el numero "<< i <<" a operar"<<endl;
        cin>>n[i]; 
    }
    cout<<"¿Que operación desea realizar?"<<endl;
    cout<<"1.- Suma \n2.- Resta \n3.-Multiplicacion \n4.-Division"<<endl;
    cin>>opc;
    switch(opc){
        case 1:
            res=0;
            for(int i=1;i<=cant;i++){
            res+=n[i];
            }
            cout<<"El resultado de la suma es:";
        break;
        case 2:
            res=0;
            for(int i=1;i<=cant;i++){
                res-=n[i];
            }
            cout<<"El resultado de la resta es:";
        break;
        case 3:
            res=1;
            for(int i=1;i<=cant;i++){
                res=res*n[i];
            }
            cout<<"El resultado de la multiplicacion es:";
        break;
        case 4:
            res=1;
            for(int i=1;i<=cant;i++){
                res=n[i]/res;
            }
            cout<<"El resultado de la division es:";
        break;

    }
    cout<<endl<<res<<endl;    
}
