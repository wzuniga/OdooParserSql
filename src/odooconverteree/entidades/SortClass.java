/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooconverteree.entidades;

import java.util.ArrayList;
import java.util.Set;

/**
 *
 * @author wzuniga
 */
public class SortClass {
    
    Graph gr;
    ArrayList<ClassOdoo> classes;
    ArrayList<ClassOdoo> dict;

    public SortClass(Graph gr, ArrayList<ClassOdoo> classes) {
        this.gr = gr;
        this.classes = classes;
        this.dict = (ArrayList<ClassOdoo>) classes.clone();
    }
    
    public ArrayList<ClassOdoo> sort(){
        ArrayList<ClassOdoo> new_classes = new ArrayList<ClassOdoo>();
        for (ClassOdoo cl : classes)
            if (gr.isWithOutParents(cl.getName()))
                new_classes.add(cl);

        classes.removeAll(new_classes);
        int i = 2;
        //System.out.println("***************");
        //System.out.println(new_classes);
        //System.out.println("***************");
        while(!classes.isEmpty()){
            ArrayList<ClassOdoo> temp = new ArrayList<ClassOdoo>();
            for (ClassOdoo cl : classes){
                //System.out.println("nivel " + cl.name);
                //System.out.println(gr.edges.get(cl.name).parents);
                //System.out.println(gr.edges.get(cl.name).parents);
                //System.out.println(new_classes);
                
                if ( areInList(gr.edges.get(cl.name).parents , new_classes)){
                    temp.add(cl);
                }
            }
            classes.removeAll(temp);
            //System.out.println(classes);
            //System.out.println(temp);
            new_classes.addAll(temp);
        }
        return new_classes;
    }

    private boolean areInList(Set<String> parents, ArrayList<ClassOdoo> new_classes) {
        for (String parent : parents){
            int i = getClassOdoo(parent);
            if(!new_classes.contains(dict.get(i)))
                return false;
        }
        return true;
    }

    private int getClassOdoo(String parent) {
        int i = 0;
        for (ClassOdoo classe : dict) {
            if (classe.name.equals(parent))
                return i;
            i++;
        }
        return -1;
    }
}
