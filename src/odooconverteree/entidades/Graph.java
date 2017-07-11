/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package odooconverteree.entidades;

import java.util.*;

public class Graph {

    public Map<String, GraphDes> edges = new TreeMap<>();

    public void addNode(String u) {
        if (!edges.containsKey(u)) {
            edges.put(u, new GraphDes());
        }
    }

    public void addEdge(String u, String v) {
        if ( u.equals("not found") || v.equals("not found")) return;
        addNode(u);
        addNode(v);
        edges.get(u).children.add(v);
        edges.get(v).parents.add(u);
    }
    
    public boolean isWithOutParents(String str){
        //System.out.println(str);
        //System.out.println(edges.get(str));
        return edges.get(str).parents.isEmpty();
    }
    
    @Override
    public String toString(){
        String str = "";
        for( String item:edges.keySet() ){
            str += "{"+item + ":" + isWithOutParents(item)+"}=" + edges.get(item) + " ";
        }
        return str;
    }
    
    public boolean haveCycles(){
        
        for(Map.Entry<String, GraphDes> item : edges.entrySet()){
            GraphDes fronItem = item.getValue();
            HashMap<String, Boolean> hm = new HashMap<String, Boolean>();
            if (recurciveFunction(item.getKey(), fronItem, hm))
                return true;
        }
        return false;
    }
    
    private boolean recurciveFunction(String name, GraphDes item, HashMap<String, Boolean> path){
        //System.out.println("Inicio " + name);
        if (path.containsKey(name)) return true;
        path.put(name, true);
        for( String it : item.children){
            //System.out.println("hijo " + it);
            boolean ans = recurciveFunction(it, edges.get(it), path);
            if (ans) return true;
            path.remove(it);
        }
        return false;
    }

    /** Usage example
    public static void main(String[] args) {
        Graph gr = new Graph();
        gr.addEdge("1", "2");
        gr.addEdge("3", "2");
        gr.addEdge("3", "4");
        gr.addEdge("5", "4");
        gr.addEdge("12", "1");
        System.out.println(gr);
        Graph g = new Graph();
         g.addEdge(0, 1);
         g.addEdge(1, 2);
         System.out.println(g.edges);
         g.removeEdge(1, 0);
         System.out.println(g.edges);
         g.removeNode(1);
         System.out.println(g.edges);
    }**/
    
    class GraphDes{
        Set<String> children = new TreeSet<String>();
        Set<String> parents = new TreeSet<String>();
        
        @Override
        public String toString(){
            return "[parent: " + parents + "-" + "children: "+children +"]";
        }
    }
}
