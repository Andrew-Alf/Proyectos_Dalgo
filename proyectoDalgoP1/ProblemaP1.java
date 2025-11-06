//Proyecto Realizado por:
//Angela Jimenez - 202210989
//Andrés Felipe Alfonso Gamba - 202210412

import java.io.*;
import java.util.*;
import java.util.stream.IntStream;

public class ProblemaP1 {
    
    public static int maxCarryReal(int k) {
        return (9 * k) / 10;
    }
    
    public static int[] crearTablaScore(int k, int maxT) {
        int[] tabla = new int[maxT + 1];

        for (int T = 0; T <= maxT; T++) {
            int q = T / 3;
            int r = T % 3;
            int s = (q + 2) / 3;
            
            if (r == 0 || s < k) {
                tabla[T] = q;
            } else {
                int m = q % 3;
                tabla[T] = q - (m == 1 ? 1 : 2);
            }
        }
        return tabla;
    }
    
    public static long resolverFestivalRobots(int n, int k, int[] valoresP) {
        int maxT = 9 * k;
        int[] tablaScore = crearTablaScore(k, maxT);
        
        int maxCarry = maxCarryReal(k) + 5;
        
        int[] digitosN;
        if (n == 0) {
            digitosN = new int[]{0};
        } else {
            List<Integer> digitosList = new ArrayList<>();
            int tempN = n;
            while (tempN > 0) {
                digitosList.add(tempN % 10);
                tempN /= 10;
            }
            digitosN = digitosList.stream().mapToInt(i -> i).toArray();
        }
        
        int numDigitos = digitosN.length;
        
        // Extender valores_p con ceros si es necesario
        int[] valoresPExtendidos = new int[numDigitos];
        for (int i = 0; i < numDigitos; i++) {
            valoresPExtendidos[i] = (i < valoresP.length) ? valoresP[i] : 0;
        }
        
        // DP usando arrays: -1 indica estado inalcanzable
        long[] dpPrev = new long[maxCarry + 1];
        Arrays.fill(dpPrev, -1);
        dpPrev[0] = 0;  // Caso base: columna 0, acarreo 0
        
        // Procesar cada columna
        for (int col = 0; col < numDigitos; col++) {
            long[] dpCurr = new long[maxCarry + 1];
            Arrays.fill(dpCurr, -1);
            
            int dP = digitosN[col];
            int PP = valoresPExtendidos[col];
            
            for (int cin = 0; cin <= maxCarry; cin++) {
                if (dpPrev[cin] == -1) {  // Estado inalcanzable
                    continue;
                }
                
                int lo = (cin - dP + 9) / 10;
                if (lo < 0) {
                    lo = 0;
                }
                int hi = Math.min(maxCarry, (9 * k + cin - dP) / 10);
                
                for (int cout = lo; cout <= hi; cout++) {
                    int T = dP - cin + 10 * cout;
                    
                    long ganancia = (long) PP * tablaScore[T];
                    
                    long nuevaCreatividad = dpPrev[cin] + ganancia;
                    if (dpCurr[cout] == -1 || dpCurr[cout] < nuevaCreatividad) {
                        dpCurr[cout] = nuevaCreatividad;
                    }
                }
            }
            
            dpPrev = dpCurr;
        }
        
        return dpPrev[0] != -1 ? dpPrev[0] : 0;
    }
    
    public static void main(String[] args) throws IOException {
        // long tiempoInicio = System.nanoTime();
        
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter pw = new PrintWriter(System.out);
        
        int numCasos = Integer.parseInt(br.readLine().trim());
        
        for (int i = 0; i < numCasos; i++) {
            String[] datos = br.readLine().trim().split(" ");
            int k = Integer.parseInt(datos[0]);  // número de celdas
            int n = Integer.parseInt(datos[1]);  // energía total
            
            // valores P0 P1 P2 P3 P4
            int[] valoresP = new int[datos.length - 2];
            for (int j = 2; j < datos.length; j++) {
                valoresP[j - 2] = Integer.parseInt(datos[j]);
            }
            
            long resultado = resolverFestivalRobots(n, k, valoresP);
            pw.println(resultado);
        }
        
        pw.flush();
        br.close();
        
        // long tiempoTotal = System.nanoTime() - tiempoInicio;
        // System.err.printf("Tiempo: %.6fs%n", tiempoTotal / 1_000_000_000.0);
    }
}
