#include <stdio.h>
#include <iostream>
#include <windows.h>

using namespace std;

void gotoxy(int x, int y);
void cuadro(int x1,int y1, int x2, int y2);

int main()
{
    float xP,yP,y[40],x[40],restasNum[40][40],restasDen[40][40],numerador[40],denominador[40],division[40],yR[40];
    int valores,i,j,opc;
    i=0;
    j=0;
   	system("COLOR B0");
   	cuadro(1,1,77,3);
   	gotoxy(20,2);cout<<"Interpolacion de lagrange\n";
    gotoxy(2,5);cout<<"Ingrese la cantidad de valores con los que quiere trabajar\n";
    gotoxy(2,6);cin>>valores;
   	system("cls");
   	cuadro(1,1,26,2+valores);
   	cuadro(1,1,13,2+valores);
    for(i=0;i<valores;i++){
        gotoxy(2,2+i);cout<<"X"<<i<<": ";
        cin>>x[i];
        gotoxy(8,2+i);cout<<"\tY"<<i<<": ";
        cin>>y[i];
        cout<<"\n";
    }
    for(i=0;i<40;i++){
        numerador[i]=1;
        denominador[i]=1;
    }
    
    //**************************************************************************************
    do{
    for(i=0;i<valores;i++){
        for(j=0;j<valores;j++){
                restasNum[i][j]=0;
                restasDen[i][j]=0;
                numerador[i]=1;
                denominador[i]=1;
                division[i]=0;
                yR[i]=0;
        }
    }
    cuadro(1,1,13,2+valores);
    cuadro(1,1,26,2+valores);
    for(i=0;i<valores;i++){
        gotoxy(2,2+i);cout<<"X"<<i<<": "<<x[i];
        gotoxy(8,2+i);cout<<"\tY"<<i<<": "<<y[i];
        cout<<"\n";
    }
    gotoxy(27,1);cout<<"Ingrese el valor de X para el cual desea hacer la interpolacion de Y:\n";
	gotoxy(27,3);cin>>xP;
    //**********************************Numerador********************************************
    for(i=0;i<valores;i++){
        for(j=0;j<valores;j++){
            if(i!=j){
                restasNum[i][j]=xP-x[j];
               
            }
           
        }
    }
    /*cout<<"Restas Numerador:\n";
    for(i=0;i<valores;i++){
        for(j=0;j<valores;j++){
            cout<<restasNum[i][j]<<"\t";
        }
        cout<<"\n";
    }*/
    for(j=0;j<valores;j++){
        for(i=0;i<valores;i++){
            if(i!=j){
                numerador[i]*=restasNum[i][j];
               
            }
           
        }
    }/*
    cout<<"Numeradores:\n";
    for(i=valores-1;i>=0;i--){
        cout<<numerador[i]<<"\n";
    }*/
    //***********************************Denominador*******************************************
    for(i=0;i<valores;i++){
        for(j=0;j<valores;j++){
            if(i!=j){
                restasDen[i][j]=x[i]-x[j];
            }
           
        }
    }/*
    cout<<"Restas Denominador:\n";
    for(i=0;i<valores;i++){
        for(j=0;j<valores;j++){
            cout<<restasDen[i][j]<<"\t";
        }
        cout<<"\n";
    }*/
    for(j=0;j<valores;j++){
        for(i=0;i<valores;i++){
            if(i!=j){
                denominador[i]*=restasDen[i][j];
               
            }
           
        }
    }
    for(i=valores-1;i>=0;i--){
        division[i]=numerador[i]/denominador[i];
    }
    for(i=0;i<valores;i++){
        yR[i]=y[i]*division[i];
        yP+=yR[i];
    }
   /*
    cout<<"Denominadores:\n";
    for(i=valores-1;i>=0;i--){
        cout<<denominador[i]<<"\n";
    }
    cout<<"Divisiones:\n";
    for(i=valores-1;i>=0;i--){
        cout<<division[i]<<"\n";
    }
    cout<<"Sumandos:\n";
    for(i=0;i<=valores;i++){
        cout<<yR[i]<<"\n";
    }*/
    gotoxy(27,5);cout<<"Resultado: "<<yP;
    gotoxy(27,7);cout<<"Desea realizar otra interpolación conservando los valores? (1.- Si/2.- No)";
    gotoxy(27,8);cin>>opc;
    system("cls");
    yP=0;
	}while(opc==1);
}

void gotoxy(int x, int y){
	HANDLE hcon;
	hcon= GetStdHandle(STD_OUTPUT_HANDLE);
	COORD dwPos;
	dwPos.X= x;
	dwPos.Y= y;
	SetConsoleCursorPosition(hcon,dwPos);
}
void cuadro(int x1,int y1, int x2, int y2){
	int i;
	for(i=x1;i<x2;i++){
		gotoxy(i,y1);printf("Ä");
		gotoxy(i,y2);printf("Ä");
	}
	for(i=y1;i<y2;i++){
		gotoxy(x1,i);printf("\263");
		gotoxy(x2,i);printf("\263");
	}
	gotoxy(x1,y1);printf("Ú");
	gotoxy(x1,y2);printf("À");
	gotoxy(x2,y1);printf("¿");
	gotoxy(x2,y2);printf("Ù");
}
