package audio_steganography;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class Extracting {
	
	public static void extract() throws IOException {
		
		Metadata f = new Metadata();
		
        File mcarrierFile = new File("C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\output.wav");
        File messageFile = new File(f.getPath());
        
        FileInputStream carrier = new FileInputStream(mcarrierFile);
        FileOutputStream message = new FileOutputStream(messageFile);
        
        byte[] carrierBuffer = new byte[(int)mcarrierFile.length()];
        
        int carrierLength;
        int messageLength = (int)f.getLength();
        
        int wav_header = 44;
        
        while ((carrierLength = carrier.read(carrierBuffer)) > 0) {
        	
            // Extract the data from the least significant bit of each byte
        	int j = 0;
        	
            for (int i = wav_header; i < carrierLength || j < messageLength; i = i + 8) {
            	
                byte data = (byte) (((carrierBuffer[i] & 0x01) << 7) | ((carrierBuffer[i + 1] & 0x01) << 6)
                		| ((carrierBuffer[i + 2] & 0x01) << 5) | ((carrierBuffer[i + 3] & 0x01) << 4)
                		| ((carrierBuffer[i + 4] & 0x01) << 3) | ((carrierBuffer[i + 5] & 0x01) << 2)
                		| ((carrierBuffer[i + 6] & 0x01) << 1) | (carrierBuffer[i + 7] & 0x01));
                
                message.write(data);
                
                j++;
                
                if (j == messageLength) break;
                
            }
        }
        
        carrier.close();
        message.close();
        
        System.out.println("Succeed to extract!\n");
        
    } // extract()
	
} // class Extracting
