package audio_steganography;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class Embedding {
	
	public static void embed(String iCarrierPath, String messagePath, String oCarrierPath) throws IOException {
		
        File nCarrierFile = new File(iCarrierPath);
        File messageFile = new File(messagePath);
        Metadata f = new Metadata(messagePath);
        
        if (nCarrierFile.length() / f.getLength() < 9) {
        	System.out.println("Failed to embed! The file is too big!");
        	return;
        }
        
        File mCarrierFile = new File(oCarrierPath);
        
        FileInputStream carrierIn = new FileInputStream(nCarrierFile);
        FileInputStream messageIn = new FileInputStream(messageFile);
        FileOutputStream carrierOut = new FileOutputStream(mCarrierFile);

        byte[] carrierBuffer = new byte[(int)nCarrierFile.length()];
        byte[] messageBuffer = new byte[(int)messageFile.length()];
        
        int carrierLength;
        int messageLegth;
        
        int wav_header = 44;
        
        while ((carrierLength = carrierIn.read(carrierBuffer)) > 0 && (messageLegth = messageIn.read(messageBuffer)) > 0) {
        	
        	int j = 0;
        	
            for (int i = 0; i < messageLegth || j < messageLegth; i = i + 8) {
            	
            	byte temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header] = (byte) ((carrierBuffer[i + wav_header] & 0xFE) | (((temp & 0x80) >> 7) & 0x01));
            	temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header + 1] = (byte) ((carrierBuffer[i + wav_header + 1] & 0xFE) | ((temp & 0x40) >> 6));
            	temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header + 2] = (byte) ((carrierBuffer[i + wav_header + 2] & 0xFE) | ((temp & 0x20) >> 5));
            	temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header + 3] = (byte) ((carrierBuffer[i + wav_header + 3] & 0xFE) | ((temp & 0x10) >> 4));
            	temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header + 4] = (byte) ((carrierBuffer[i + wav_header + 4] & 0xFE) | ((temp & 0x08) >> 3));
            	temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header + 5] = (byte) ((carrierBuffer[i + wav_header + 5] & 0xFE) | ((temp & 0x04) >> 2));
            	temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header + 6] = (byte) ((carrierBuffer[i + wav_header + 6] & 0xFE) | ((temp & 0x02) >> 1));
            	temp = (byte)messageBuffer[j];
            	carrierBuffer[i + wav_header + 7] = (byte) ((carrierBuffer[i + wav_header + 7] & 0xFE) | (temp & 0x01));
            	
            	j++;
            	
            } // for
            
            carrierOut.write(carrierBuffer, 0, carrierLength);
            carrierOut.flush();
            
        } // while
        
        carrierIn.close();
        messageIn.close();
        carrierOut.close();
        
        System.out.println("Succeed to embed!\n");
        
    } // embed(String iCarrierPath, String messagePath, String oCarrierPath)
	
} // class Embedding
