/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooParserSql;

import java.util.ArrayList;
import odooconverteree.entidades.ClassOdoo;
import odooconverteree.entidades.FieldOdoo;

/**
 *
 * @author Ana Flavia Begazo
 */
public class AdapterMySql {
    
    ArrayList<FieldOdoo> fields = new ArrayList<FieldOdoo>();
    ArrayList<FieldOdoo> relations = new ArrayList<FieldOdoo>();
    String reservedWords [] = {
        "option"
    };
    
    public String createTable(ClassOdoo clOd){
        separateFields(clOd);
        String sql = "CREATE TABLE " + clOd.getName() + "(\n";
        sql += generateAtribute(new FieldOdoo("id", "Integer"), false);
        for (int i = 0; i < fields.size(); i++) {
            FieldOdoo fieldOdoo = fields.get(i);
            if(isRelation(fieldOdoo.getTipo())){
                relations.add(fieldOdoo);
                continue;
            }
            verify(fieldOdoo);
            sql += generateAtribute(fieldOdoo, i == fields.size()-1);
        }
        
        addRelationalFields(sql);
        
        sql += ")\n";
        return sql;
    }
    
    private String generateAtribute(FieldOdoo flOd, boolean last){
        return flOd.getField() + " " + getTypeRow(flOd.getTipo()) + (last ? "" : ",")  + "\n";
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
                fieldOdoo.setField(fieldOdoo.getField()+"changed");
        }
    }

    private String addRelationalFields(String sql) {
        
        return sql;
    }
}
