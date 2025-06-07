import java.util.*;

public class TaskValidator {

    public static int findValidTask(List<Integer> difficulty) {
        int n = difficulty.size();

        long[] evenPrefix = new long[n + 1];
        long[] oddPrefix = new long[n + 1];

        // Construir prefix sums
        for (int i = 0; i < n; i++) {
            evenPrefix[i + 1] = evenPrefix[i];
            oddPrefix[i + 1] = oddPrefix[i];

            if (i % 2 == 0) {
                evenPrefix[i + 1] += difficulty.get(i);
            } else {
                oddPrefix[i + 1] += difficulty.get(i);
            }
        }

        // Evaluar cada posible j (1-based)
        for (int j = 1; j <= n; j++) {
            int j0 = j - 1; // 0-based index para j

            for (int i = 1; i <= j; i++) {
                int i0 = i - 1; // 0-based index para i

                long evenSum = 0;
                long oddSum = 0;

                if ((i0 % 2) == (j0 % 2)) {
                    // Mismo tipo de paridad
                    if (j0 - i0 < 1) {
                        continue;
                    } else {
                        evenSum = evenPrefix[j0 + 1] - evenPrefix[i0];
                        oddSum = oddPrefix[j0 + 1] - oddPrefix[i0];
                    }
                } else {
                    // Paridad distinta
                    if (j0 - i0 < 1) {
                        continue;
                    } else {
                        evenSum = evenPrefix[j0] - evenPrefix[i0];
                        oddSum = oddPrefix[j0 + 1] - oddPrefix[i0];
                    }
                }

                if (evenSum == oddSum) {
                    return j; // índice 1-based del primer válido
                }
            }
        }

        return -1; // No se encontró tarea válida
    }

    public static void main(String[] args) {
        // Entrada fija equivalente a:
        // 5
        // 9
        // 1
        // 4
        // 9
        // 6

        int n = 5;
        List<Integer> difficulty = List.of(9, 1, 4, 9, 6);

        int result = TaskValidator.findValidTask(difficulty);
        System.out.println(result);  // Esperado: 5
    }
}
