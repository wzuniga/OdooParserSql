/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooconverteree.entidades;

/**
 *
 * @author Ana Flavia Begazo
 */
public class FieldOdoo {
    String field;
    String tipo;
    String related;

    public FieldOdoo(String field, String tipo) {
        this.field = field;
        this.tipo = tipo;
        this.related = null;
    }
    
    public void setRelated(String rel){
        this.related = rel;
    }
    
    @Override
    public String toString() {
        if(related == null)
            return "{"+field + "," + tipo + '}';
        return "{"+field + "," + tipo + ','+related+'}';
    }
    
    
}
