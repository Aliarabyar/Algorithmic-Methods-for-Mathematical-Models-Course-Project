// PLEASE ONLY CHANGE THIS FILE WHERE INDICATED.
// Ali Arabyarmohammadi

int n = ...;
int m = ...;

range V = 1..n;
range W = 1..m;

float G[V][V] = ...; // The matrix is symmetric as the graph is undirected.
float H[W][W] = ...; // The matrix is symmetric as the graph is undirected.

// Define here your decision variables and any other auxiliary data.
// You can run an execute block if needed.


// auxiliary variables
float BG[V][V];  // A symmetric adjacency matrix of G (0 and 1) helpful in constraints.
float BH[W][W];  // A symmetric adjacency matrix of H (0 and 1) helpful in constraints.
float cost[V][V][W][W]; // Defined to calculate absolute differences of weights.
 
 
// Desicion variables
dvar boolean a[W][V];  
dvar boolean b[W][W][V][V]; 




 execute {
    
    	// Filling the auxiliary matrix  BG
        for (var u in V) {
	   	for (var t in V) {     
  		   if (G[u][t] > 0 ) BG[u][t]=1;
    	}
	    }
	     
	     
	    // Filling the auxiliary matrix  BH 
        for (var x in W) {
	   	for (var y in W) { 
  	       if (H[x][y] > 0 ) BH[x][y]=1;
    	}
	    }
	     
	     
	    // Calculate absolute differences of weights. 
	    for (var u in V) {
	   	for (var t in V) {     
  	    for (var x in W) {
	   	for (var y in W) { 
  	       cost[u][t][x][y]=  Opl.abs( G[u][t] -  H[x][y]) ;
    	}
	    }
    	}
	    }  
	     
  }    
 
 
 
 
minimize 0.5 * sum(u  in V, t in V,x in W, y in W) b[x][y][u][t] * cost[u][t][x][y]; // Write here the objective function.



subject to {

 
    // Write here the constraints.
	
	// Please find the explanation for each constraints in the report.
	
	
    forall (x in W) {
    sum(u in V ) a[x][u] == 1;
    }	
 
 
	forall (u in V) {
    sum(x in W ) a[x][u] <= 1;
    }	
	
	 
    forall (x in W, y in W) {
       	  sum(u  in V, t in V ) b[x][y][u][t] * BG[u][t] == BH[x][y] ;
 	}
 

    forall (x in W, y in W, t in V ) {
       	  sum(u  in V ) b[x][y][u][t] * BG[u][t] <= (a[x][t] + a[y][t]) * BH[x][y] ;
 	}

  
     forall (x in W, y in W, u in V ) {
       	  sum( t in V ) b[x][y][u][t] * BG[u][t] <= (a[x][u] + a[y][u])  * BH[x][y] ;
 	}
 
 
     forall ( t in V, u in V ) {
         sum(x in W ) (a[x][u] + a[x][t])  -  sum( x in W, y in W ) b[x][y][u][t] * BH[x][y]  <=  2 - BG[u][t] ;
    }
 

   }
 
 

execute {
     
    for (var x in W) {
	var fx = 0;
  	for (var u in V) {
  	    if (a[x][u] == 1) fx = u;
    	}
	writeln("f(" + x + ") = " + fx);
    }
}

 