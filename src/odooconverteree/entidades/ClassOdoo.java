/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooconverteree.entidades;

import java.util.ArrayList;

/**
 *
 * @author wzuniga
 */
public class ClassOdoo {
    String name;
    String tableName;
    public ArrayList <FieldOdoo> atributos;

    public ClassOdoo(String name) {
        this.name = name;
        atributos = new ArrayList<FieldOdoo>();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
    
    public String getTableName() {
        return tableName;
    }

    public void setTableName(String name) {
        this.tableName = name;
    }

    public ArrayList<FieldOdoo> getAtributos() {
        return atributos;
    }

    public void setAtributos(ArrayList<FieldOdoo> atributos) {
        this.atributos = atributos;
    }
    
    public String toString(){
        return name + "-"+ tableName + ":" + atributos;
    }
    
}
