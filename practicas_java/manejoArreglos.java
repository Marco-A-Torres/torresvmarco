import java.util.Scanner;

public class manejoArreglos{
    public static void main(String[] args){
        Scanner leer = new Scanner(System.in);

        String[] nombres = new String[10];
        float[][] calif = new float[10][3];
        float highst=0, lowst=100, sumProm=0, prom;
        int cantA=0,cantCal=0, alhst=0, alwst=0;
        System.out.println("Ingrese la cantidad de alumnos que desea capturar:");
        cantA = leer.nextInt();
        leer.nextLine();
        for(int i=0;i<cantA;i++){
            System.out.println("Ingrese el nombre del alumno #"+i+":");
            nombres[i]= leer.nextLine();
            for(int j=0;j<3;j++){
                System.out.println("Ingrese la calificación No. "+j+" del alumno "+i+":");
                calif[i][j]=leer.nextFloat();
                leer.nextLine();
                sumProm+=calif[i][j];
                cantCal++;
                if(calif[i][j]>highst){
                    highst=calif[i][j];
                    alhst=i;
                }else if(calif[i][j]<lowst){
                    lowst=calif[i][j];
                    alwst=i;
                }
                
            }
        }
        prom=sumProm/cantCal;
        System.out.println("El promedio de las calificaciones ingresadas es: "+prom);
        System.out.println("El alumno con la calificación más alta fue "+nombres[alhst]+"con "+highst);
        System.out.println("El alumno con la calificación más baja fue "+nombres[alwst]+"con "+lowst);
    }
}