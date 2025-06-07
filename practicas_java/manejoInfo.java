import java.util.Scanner;

public class manejoInfo{
    public static void main(String[] args){
        Scanner leer = new Scanner(System.in);

        String nombre, carrera, mensaje;

        System.out.println("Ingrese su nombre:");
        nombre = leer.nextLine();

        System.out.println("Ingrese su carrera:");
        carrera = leer.nextLine();

        System.out.println("Ingrese el mensaje que quiere comunicar:");
        mensaje = leer.nextLine();
        
        System.out.println("Los datos del usuario son los siguientes");
        System.out.println("Nombre: "+nombre);
        System.out.println("Carrera: "+carrera);
        System.out.println("Mensaje: "+mensaje);

    }
}