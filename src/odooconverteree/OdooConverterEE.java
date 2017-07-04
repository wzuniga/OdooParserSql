/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooconverteree;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

/**
 *
 * @author wzuniga
 */
public class OdooConverterEE {
    
    static State state = State.OUTCLASS;
    
    public static void main(String [] args) {
      File archivo = null;
      FileReader fr = null;
      BufferedReader br = null;
      String file = "C:\\archivo.txt";

      try {
         // Apertura del fichero y creacion de BufferedReader para poder
         // hacer una lectura comoda (disponer del metodo readLine()).
         archivo = new File (file);
         fr = new FileReader (archivo);
         br = new BufferedReader(fr);

         // Lectura del fichero
         String linea;
         while((linea=br.readLine())!=null){
             System.out.println(linea);
             
         }
      }
      catch(Exception e){
         e.printStackTrace();
      }finally{
         try{                    
            if( null != fr ){   
               fr.close();     
            }                  
         }catch (Exception e2){ 
            e2.printStackTrace();
         }
      }
   }
    
    public static void analizeLine(String str){
        String strClean = str.trim();
        if(!isComment(strClean)){
            if(state == State.INCLASS){
                analizeInClass(strClean);
            }else{
                if(strClean.substring(0, strClean.indexOf(" ")).equals("class")){
                    
                }
            }
        }
    }
    
    public static void analizeInClass(String str){
        
    }
    
    public static void analizeOutClass(String str){
        
    }
    
    public static boolean isComment(String str){
        return str.substring(0,1).equals("#");
    }
    
}
