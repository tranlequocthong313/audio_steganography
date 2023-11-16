package audio_steganography;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
public class Extracting {
	public static void extract() throws IOException {
		Metadata f = new Metadata();
        File audioFile = new File("C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\output.wav");
        File outputFile = new File(f.getPath());
        FileInputStream audioIn = new FileInputStream(audioFile);
        FileOutputStream out = new FileOutputStream(outputFile);
        byte[] audioBuffer = new byte[(int)audioFile.length()];
        int audioLength;
        int outputLength = (int)f.getLength();
        int wav_header = 44;
        while ((audioLength = audioIn.read(audioBuffer)) > 0) {
            // Extract the data from the least significant bit of each byte
        	int j = 0;
            for (int i = wav_header; i < audioLength && j < outputLength; i = i + 8) {
                byte data = (byte) (((audioBuffer[i] & 0x01) << 7) | ((audioBuffer[i + 1] & 0x01) << 6)
                		| ((audioBuffer[i + 2] & 0x01) << 5) | ((audioBuffer[i + 3] & 0x01) << 4)
                		| ((audioBuffer[i + 4] & 0x01) << 3) | ((audioBuffer[i + 5] & 0x01) << 2)
                		| ((audioBuffer[i + 6] & 0x01) << 1) | (audioBuffer[i + 7] & 0x01));
                out.write(data);
                j++;
                //System.out.print(data);
            }
        }
        audioIn.close();
        out.close();
        System.out.println("Succeed to extract!\n");
    }
}
