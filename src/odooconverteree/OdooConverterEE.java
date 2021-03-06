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
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import odooParserSql.AdapterMySql;
import odooconverteree.entidades.FieldOdoo;

/**
 *
 * @author wzuniga
 */
public class OdooConverterEE {

    static State state = State.OUTCLASS;
    static ArrayList<ClassOdoo> classes = new ArrayList<ClassOdoo>();
    static int counterBlank = 0;

    public String start(String [] files) {
        File archivo = null;
        FileReader fr = null;
        BufferedReader br = null;
        String sql = "";

        try {
            for (int i = 0; i < files.length; i++) {
                archivo = new File(files[i]);
                fr = new FileReader(archivo);
                br = new BufferedReader(fr);

                // Lectura del fichero
                String linea;
                while ((linea = br.readLine()) != null) {
                    //System.out.println(linea);
                    analizeLine(linea);
                }
                state = State.OUTCLASS;
                counterBlank = 0;
            }
            
            //print(classes.toString());
            write("class.txt", classes.toString());
            //print("\n");
            //print("\n");
            //print("\n");
            //print("\n");
            
            //print(classes.toString());
            AdapterMySql adapterMySql = new AdapterMySql(classes, "Test2");
            classes = adapterMySql.sortClassOdoo(classes);
            adapterMySql.setClass(classes);
            sql = adapterMySql.createDataBase();
            for (ClassOdoo classe : classes) {
                sql += adapterMySql.createTables(classe);
            }
            //print(sql);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (null != fr) {
                    fr.close();
                }
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        }
        return sql;
    }

    public State analizeLine(String str) {
        String strClean = str.trim();
        //System.out.println(strClean);
        if (!isBlank(strClean) && !isComment(strClean)) {
            if (state == State.INCLASS) {
                analizeInClass(strClean);
            } else {
                if (state == State.RELATION) {
                    String rel = strClean.split("\\'")[1];
                    insertInLastItemRelation(rel);
                    state = State.INCLASS;
                } else if (strClean.substring(0, strClean.indexOf(" ")).equals("class")) {
                    state = State.INCLASS;
                    classes.add(new ClassOdoo(getNameClass(strClean)));
                }
            }
        }
        return state;
    }

    public void analizeInClass(String str) {
        if (!isComment(str) && isField(str)) {
            String varch[] = str.split(" ");
            String temp = varch[2].split("\\.")[1];
            String tipo = temp.substring(0, temp.indexOf("("));
            isRelation(tipo);
            insertInLastItem(varch[0], tipo);
        } else {
            //Si es _name
            String varch[] = str.split(" ");
            if (varch[0].equals("_name") || varch[0].equals("_inherit")) {
                classes.get(classes.size() - 1).setTableName(varch[2].split("\\'")[1]);
            }
        }
    }

    public void analizeOutClass(String str) {

    }

    public boolean isComment(String str) {
        return str.substring(0, 1).equals("#");
    }

    public boolean isBlank(String str) {
        boolean ans = str.isEmpty();
        if (ans) {
            if (counterBlank == 1) {
                state = State.OUTCLASS;
                counterBlank = 0;
            } else {
                counterBlank++;
            }
        } else {
            counterBlank = 0;
        }
        return ans;
    }

    public boolean isField(String str) {
        String arr[] = str.split(" ");
        if (arr.length >= 3 && arr[2].indexOf("fields") >= 0) {
            //agregar aqui para obtener tipo de Dato
            //System.out.println(arr[2].split("\\.")[0]);
            return arr[2].split("\\.")[0].equals("fields");
        }
        return false;
    }

    public boolean isRelation(String type) {
        if (type.equals("Many2one") || type.equals("One2many") || type.equals("Many2many")) {
            state = State.RELATION;

            return true;
        }
        return false;
    }

    public String getNameClass(String str) {
        String temp = str.split(" ")[1];

        return temp.substring(0, temp.indexOf("("));
    }

    public void insertInLastItem(String name, String type) {
        if (state == State.OUTCLASS) {
            return;
        }
        classes.get(classes.size() - 1).atributos.add(new FieldOdoo(name, type));

    }

    public void insertInLastItemRelation(String rel) {
        if (state == State.OUTCLASS) {
            return;
        }
        ArrayList<FieldOdoo> temp = classes.get(classes.size() - 1).atributos;
        temp.get(temp.size() - 1).setRelated(rel);
    }

    public void print(String str) {
        System.out.println(str);
    }
    
    public void write(String name, String txt){
        FileWriter fichero = null;
        PrintWriter pw = null;
        try
        {
            fichero = new FileWriter(name);
            pw = new PrintWriter(fichero);
            pw.println(txt);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
           try {
           // Nuevamente aprovechamos el finally para 
           // asegurarnos que se cierra el fichero.
           if (null != fichero)
              fichero.close();
           } catch (Exception e2) {
              e2.printStackTrace();
           }
        }
    }
}
