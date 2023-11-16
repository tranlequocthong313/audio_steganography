package audio_steganography;
import java.io.File;
public class Metadata {
	static private String name;
	static private String absolutePath;
	static private long length;
	public Metadata() {
		return;
	}
	public Metadata(String Path) {
		File f = new File(Path);
        if(f.exists()){
            name = f.getName();
            absolutePath = f.getAbsolutePath();
            length = f.length();
        }else{
            System.out.println("The File does not exist");
        }
	}
	public String getName() {
		return name;
	}
	public String getPath() {
		return absolutePath;
	}
	public long getLength() {
		return length;
	}
	
}
