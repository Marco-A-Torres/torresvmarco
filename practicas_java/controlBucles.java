import java.util.Scanner;

public class controlBucles{
    public static void main(String[] args){
        Scanner leer = new Scanner(System.in);

        int i,lim,sum=0;
        String loop="null";
        do{
            System.out.println("Ingrese el numero limite:");
            lim = leer.nextInt();
            leer.nextLine();
            System.out.println("Numeros pares del 0 a "+lim+":");
            for(i=0;i<=lim;i++){
                if((i % 2)==0 && i!=0){
                    System.out.println(i);
                }
            }
            i=0;
            sum=0;
            while(i<=lim){
                if(i % 2 != 0){
                    sum+=i;
                }
                i++;
            }
            System.out.println("La suma de los numeros impares del 0 al "+lim+" es:"+sum);
            System.out.println("¿Desea ingresar un nuevo numero? (S/N)");
            loop=leer.nextLine();
        }while(loop.equals("s")||loop.equals("S"));
        
    }
}