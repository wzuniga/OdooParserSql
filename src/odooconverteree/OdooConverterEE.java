/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooconverteree;

import odooconverteree.entidades.ClassOdoo;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import odooconverteree.entidades.FieldOdoo;

/**
 *
 * @author wzuniga
 */
public class OdooConverterEE {
    
    static State state = State.OUTCLASS;
    static ArrayList <ClassOdoo> classes = new ArrayList<ClassOdoo>();
    static int counterBlank = 0;
    
    public static void main(String [] args) {
      File archivo = null;
      FileReader fr = null;
      BufferedReader br = null;
      String file = "C:\\Users\\Ana Flavia Begazo\\Documents\\NetBeansProjects\\OdooParserSql\\test\\models\\observacion.py";

      try {
         // Apertura del fichero y creacion de BufferedReader para poder
         // hacer una lectura comoda (disponer del metodo readLine()).
         archivo = new File (file);
         fr = new FileReader (archivo);
         br = new BufferedReader(fr);

         // Lectura del fichero
         String linea;
         while((linea=br.readLine())!=null){
             //System.out.println(linea);
             analizeLine(linea);
         }
         print(classes.toString());
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
    
    public static State analizeLine(String str){
        String strClean = str.trim();
        System.out.println(strClean);
        if(!isBlank(strClean) && !isComment(strClean)){
            if(state == State.INCLASS){
                analizeInClass(strClean);
            }else{
                if( state == State.RELATION ){
                    String rel = strClean.split("\\'")[1];
                    insertInLastItemRelation(rel);
                    state = State.INCLASS;
                }
                else if(strClean.substring(0, strClean.indexOf(" ")).equals("class")){
                    state = State.INCLASS;
                    classes.add(new ClassOdoo(getNameClass(strClean)));
                }
            }
        }
        return state;
    }
    
    public static void analizeInClass(String str){
        if(!isComment(str) && isField(str)){
            String varch [] = str.split(" ");
            String temp = varch[2].split("\\.")[1];
            String tipo = temp.substring(0, temp.indexOf("("));
            isRelation(tipo);
            insertInLastItem(varch[0], tipo);
        }else{
            //Si es _name
            String varch [] = str.split(" ");
            if(varch[0].equals("_name")){
                classes.get(classes.size()-1).setTableName(varch[2].split("\\'")[1]);
            }
        }
    }
    
    public static void analizeOutClass(String str){
        
    }
    
    public static boolean isComment(String str){
        return str.substring(0,1).equals("#");
    }
    
    public static boolean isBlank(String str){
        boolean ans = str.isEmpty();
        if (ans)
            if (counterBlank == 1){
                state = State.OUTCLASS;
                counterBlank = 0;
            }
            else
                counterBlank++;
        else
            counterBlank = 0;
        return ans;
    }
    
    public static boolean isField(String str){
        String arr [] = str.split(" ");
        if(arr.length >= 3 && arr[2].indexOf("fields") >= 0){
            //agregar aqui para obtener tipo de Dato
            System.out.println(arr[2].split("\\.")[0]);
            return arr[2].split("\\.")[0].equals("fields");
        }
        return false;
    }
    
    public static boolean isRelation(String type){
        if( type.equals("Many2one") || type.equals("One2many") || type.equals("Many2many")){
            state = State.RELATION;
            
            return true;
        }
        return false;
    }
    
    public static String getNameClass(String str){
        String temp = str.split(" ")[1];
        
        return temp.substring(0, temp.indexOf("("));
    }
    
    public static void insertInLastItem(String name, String type){
        if( state == State.OUTCLASS )
            return;      
        classes.get(classes.size()-1).atributos.add(new FieldOdoo(name, type));
        
    }
    
    public static void insertInLastItemRelation(String rel){
        if( state == State.OUTCLASS )
            return;
        ArrayList<FieldOdoo> temp =  classes.get(classes.size()-1).atributos;
        temp.get(temp.size() -1).setRelated(rel);
    }
    
    public static void print(String str){
        System.out.println(str);
    }
}
