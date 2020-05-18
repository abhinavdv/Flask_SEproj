import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.List;

public class process_gen{
	public static void main(String[] args) {
		int writers=4,readers=4;
		for(int i=1;i<=writers;i++) {
		 try {
		      FileWriter logwtr = new FileWriter(("writers"+ i +".java"),true);
		      System.out.println("writer"+ i +".java");
		      BufferedWriter bw = new BufferedWriter(logwtr);
		      PrintWriter pw = new PrintWriter(bw);
		      System.out.println("creating a new line");
		      
		      pw.println("import java.rmi.registry.*;");
		      pw.println("import java.rmi.registry.LocateRegistry;");
		      pw.println("import java.rmi.RemoteException;"); 
		      pw.println("import java.rmi.server.UnicastRemoteObject;");
		      pw.println("import java.sql.Connection;");
		      pw.println("import java.sql.DriverManager;");
		      pw.println("import java.sql.Statement;");
		      pw.println("import java.util.ArrayList;");
		      pw.println("import java.util.LinkedList;");
		      pw.println("import java.util.List;");
		      pw.println("import java.util.Queue;");
		      pw.println("import java.util.Random;");
		      pw.println("import java.io.BufferedWriter;");
		      pw.println("import java.io.FileWriter;");
		      pw.println("import java.io.IOException;");
		      pw.println("import java.io.PrintWriter;");
		      pw.println("import java.rmi.*;");
		      
		      
		      
		      
		      pw.println("//------------------headers----------------------");
		      
		      
		   
		      pw.println("	public class process"+i +" extends container"+i+" {");
		      pw.println("		public process"+ i +"() {}");
		      pw.println("		public static void main(String args[]) {"); 
		      pw.println("			List<Student> list = null;");
		      pw.println("			String insert=\"\";");
		      pw.println("			int x=0;");
		      pw.println("			int y=0;");
		      pw.println("			try {");
		      pw.println("			Class.forName(\"com.mysql.jdbc.Driver\");");
		      pw.println("			Connection conn = DriverManager.getConnection(\"jdbc:mysql://localhost:3306/rmi"+i+"\", \"newuser\", \"password\");");
		      pw.println("			Statement stmt = conn.createStatement();");
		      pw.println("			container"+i+" obj = new container"+i+"(); ");
		      pw.println("			hello stub"+i+" = (hello) UnicastRemoteObject.exportObject(obj, 0);");
		      pw.println("			Registry registry = LocateRegistry.getRegistry(); ");
		      pw.println("			registry.bind(\"Hello"+i+"\", stub"+i+");  ");
		      pw.println("			System.out.println(\"Server ready\");");
		      pw.println("			hello stub_self"+i+" = (hello) registry.lookup(\"Hello"+i+"\");");
		      pw.println("			Thread.sleep(3000);");
		      for(int j=1;j<=writers;j++) {
		    	  if(j!=i)
		    		  pw.println("			hello stub_s"+j+" = (hello) registry.lookup(\"Hello"+j+"\");");
		      }	
		      
		      pw.println("			System.out.println(\"lookup server\");");
		      
		      
		 
		     pw.println("//-----------------------basics done---------------");
		      
		      
		      
		      pw.println("int t =0;");
		      pw.println("int t1=0;");
		      pw.println(" Thread.sleep(200);");
		      pw.println("while(true) {");
		      pw.println("if(x<10) {");
		      pw.println(" x++;");
		      pw.println("while(t<10 || (stub_self" + i + ".dbstatus(0)!=0 || stub_self" + i + ".dbstatus(1)!=0 || stub_self" + i + ".dbstatus(2)!=0 || stub_self"+i+".dbstatus(3)!=0)) {");
		      pw.println("if(t<10) {");
		      for(int j=0;j<=writers;j++) {
		    	  
		      }
		      
		      
		      
		      
		      pw.println("if(stub_self2.dbstatus(1) == 0 && stub_s1.dbstatus(1) == 0 && stub_s3.dbstatus(1) == 0 && stub_s4.dbstatus(1) == 0 ) {");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      pw.println("");
		      
		      
		      
		      
		      
		      
		         
//		         stub_self.addStudent(t);
		        
		         
		         
		         
		             
		            		 
		//-----------------------------------------------------------------------WRITING----------------------------------------------------------             
		             
		            
		
		
		
	}
		 catch (IOException e) {
			      System.out.println("An error occurred.");
			      e.printStackTrace();
			    }
}
	}
}
	