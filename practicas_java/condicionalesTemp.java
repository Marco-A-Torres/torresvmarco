import java.util.Scanner;

public class condicionalesTemp{
    public static void main(String[] args){
        Scanner leer = new Scanner(System.in);

        float temp;
        int opc;
        String nombre="No registrado", carrera="No registrado", mensaje="No registrado", loop="null" ;

        do{
            System.out.println("¿Que opción desea realizar?\n 1.- Ingresar información 2.- Comparacon de temperatura");
            opc = leer.nextInt();
            leer.nextLine();
            switch(opc){
                case 1:
                    System.out.println("Ingrese su nombre:");
                    nombre=leer.nextLine();
                    System.out.println("Ingresa tu carerra:");
                    carrera=leer.nextLine();
                    System.out.println("Ingrese el mensaje a mostrar:");
                    mensaje=leer.nextLine();

                    System.out.println("Su nombre es: "+nombre);
                    System.out.println("Su carrera es: "+carrera);
                    System.out.println("El mensaje a transmitir es: "+mensaje);
                break;
                case 2:
                    System.out.println("Ingrese la temperatura a comparar y a convertir");
                    temp= leer.nextFloat();
                    leer.nextLine();
                    if(temp<0){
                        System.out.println("Temperatura bajo cero");
                    }else if(temp>0 && temp<20){
                        System.out.println("Temperatura fria");
                    }else if(temp>20 && temp<30){
                        System.out.println("Temperatura templada");
                    }else if(temp>30){
                        System.out.println("Temperatura caliente");
                    }else{
                        System.out.println("Temperatura inválida");
                    }
                break;
            }
            System.out.println("¿Desea realizar la operación de nuevo? (S/N)");
            loop=leer.nextLine();


        }while(loop.equals("s") || loop.equals("S"));
        
    }
}