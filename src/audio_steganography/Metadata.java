package audio_steganography;

import java.io.File;

public class Metadata {
	
	// Variables
	static private String name;
	static private String absolutePath;
	static private long length;
	
	// This constructor method does not do anything
	public Metadata() {
		
		return;
		
	} // Metadata()
	
	// This constructor method get the metadata of the file
	public Metadata(String Path) {
		
		File f = new File(Path);
		
        if(f.exists()){
            name = f.getName();
            absolutePath = f.getAbsolutePath();
            length = f.length();
        } // if
        
        else{
            System.out.println("The File does not exist");
        } // else
        
	} // Metadata(String Path)
	
	// This method return the name of the file
	public String getName() {
		
		return name;
		
	} // getName()
	
	// This method return the path of the file
	public String getPath() {
		
		return absolutePath;
		
	} // getPath()
	
	// This method return the length of the file 
	public long getLength() {
		
		return length;
		
	} // getLength()
	
} // class Metadata