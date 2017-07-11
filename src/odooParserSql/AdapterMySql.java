/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooParserSql;

import java.util.ArrayList;
import odooconverteree.OdooConverterEE;
import odooconverteree.entidades.ClassOdoo;
import odooconverteree.entidades.FieldOdoo;
import odooconverteree.entidades.Graph;
import odooconverteree.entidades.SortClass;

/**
 *
 * @author wzuniga
 */
public class AdapterMySql {
    
    private ArrayList <ClassOdoo> classes = new ArrayList<ClassOdoo>();
    private String dataBaseName;
    public String reservedWords [] = {"option"};
    
    private ArrayList<FieldOdoo> fields;
    private ArrayList<FieldOdoo> relations;

    public AdapterMySql(ArrayList <ClassOdoo> classes, String name) {
        this.classes = classes;
        this.dataBaseName = name;
        this.fields = new ArrayList<FieldOdoo>();
        this.relations = new ArrayList<FieldOdoo>();
    }
    
    public void setClass(ArrayList <ClassOdoo> classes){
        this.classes = classes;
    }
    
    public String createDataBase(){
        return "CREATE DATABASE " + dataBaseName + ";\nUSE " + dataBaseName + ";\n";
    }
    
    public String createTables(ClassOdoo clOd){
        separateFields(clOd);
        String sql = "CREATE TABLE " + clOd.getName() + "(\n";
        sql += generateAtribute(new FieldOdoo("id", "Integer"));
        for (int i = 0; i < fields.size(); i++) {
            FieldOdoo fieldOdoo = fields.get(i);
            if(isRelation(fieldOdoo.getTipo())){
                relations.add(fieldOdoo);
                continue;
            }
            verify(fieldOdoo);
            sql += generateAtribute(fieldOdoo);
        }
        
        sql += addRelationalFields();
        sql += "PRIMARY KEY (id)\n";
        sql += ")ENGINE=INNODB;\n\n";
        clean();
        return sql;
    }
    
    private String generateAtribute(FieldOdoo flOd){
        return flOd.getField() + " " + getTypeRow(flOd.getTipo()) + "," + "\n";
    }
    
    private String getTypeRow(String type){
        String code = null;
        switch(type){
            case "Char": code = "VARCHAR(10)"; break;
            case "Text": code = "VARCHAR(10)"; break;
            case "Float": code = "FLOAT"; break;
            case "Integer": code = "INT"; break;
            case "Boolean": code = "tinyint(1)"; break;
            case "Date": code = "DATE"; break;
            case "Selection": code = "VARCHAR(10)"; break;
            case "Binary": code = "BLOB"; break;
        }
        return code;
    }
    
    private boolean isRelation(String type){
        return type.equals("Many2one") || type.equals("One2many") || type.equals("Many2many");
    }
    
    private void separateFields(ClassOdoo clOd){
        for (int i = 0; i < clOd.atributos.size(); i++) {
            FieldOdoo fieldOdoo = clOd.atributos.get(i);
            (isRelation(fieldOdoo.getTipo())?relations:fields).add(fieldOdoo);
        }
    }
    
    private void verify(FieldOdoo fieldOdoo){
        for (int i = 0; i < reservedWords.length; i++) {
            if(fieldOdoo.getField().equals(reservedWords[i]))
                fieldOdoo.setField(fieldOdoo.getField()+"_changed");
        }
    }

    private String addRelationalFields() {
        String sql = "";
        
        for (int i = 0; i < relations.size(); i++) {
            FieldOdoo item = relations.get(i);
            if (item.getTipo().equals("Many2one")){
                sql += item.getField() + " INT,"  + "\n";
            }
        }
        for (int i = 0; i < relations.size(); i++) {
            FieldOdoo item = relations.get(i);
            if (item.getTipo().equals("Many2one")){
                sql += "FOREIGN KEY ("+item.getField()+") REFERENCES "+getTableName(item.getRelated())+"(id)";
                sql += ",\n";
            }
        }
        return sql;
    }
    
    public String getTableName(String find){
        for (ClassOdoo clOd : classes) {
            if(clOd.getTableName().equals(find)){
                return clOd.getName();
            }
        }
        return "not found";
    }
    
    private boolean existMany2One(){
        for (int i = 0; i < relations.size(); i++) 
            if (relations.get(i).getRelated().equals("Many2one"))
                return true;
        return false;
    }

    private void clean() {
        fields = new ArrayList<FieldOdoo>();
        relations = new ArrayList<FieldOdoo>();
    }
    
    public ArrayList<ClassOdoo> sortClassOdoo(ArrayList<ClassOdoo> classes){
        Graph gr = new Graph();
        
        for (ClassOdoo classe : classes) {
            ArrayList<FieldOdoo> local_relations = new ArrayList<FieldOdoo>();
            for (FieldOdoo fieldOdoo : classe.atributos) 
                if (isRelation(fieldOdoo.getTipo()) && fieldOdoo.getTipo().equals("Many2one"))  local_relations.add(fieldOdoo);
            gr.addNode(classe.getName());
            for (FieldOdoo item:local_relations )
                gr.addEdge(getTableName(item.getRelated()), classe.getName() );//  classe.getName(), item.getRelated());
        }
        OdooConverterEE.write("graph.txt", gr.toString());
        //System.out.println(gr);
        
        SortClass sc = new SortClass(gr, classes);
        //System.out.println("????????????????????????????????");
        boolean bl = gr.haveCycles();
        if (bl){
            System.out.println("Tiene ciclos - revisar");
            System.exit(0);
        }
        return sc.sort();
    }

}
