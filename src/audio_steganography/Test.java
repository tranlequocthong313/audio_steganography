package audio_steganography;

public class Test {

	public static void main(String[] args) {
		byte a = (byte) 0x01;
		byte b = (byte) 0x80;
		System.out.println((byte)a);
		System.out.println((byte)b);
		byte c = (byte)((b >> 7) & 0x01);
		byte d = (byte)(a << 7);
		System.out.println((byte)c);
		System.out.println((byte)d);
		
		if ((byte)128 == (byte)0x80) System.out.print(true); else System.out.print(false);
		System.out.println(Byte.compareUnsigned((byte) (b >> 7), a));
	}

}
/*
 *0: 0000 0001: 1 t
 *1: 0000 0010: 2 t
 *2: 0000 0100: 4 t
 *3: 0000 1000: 8 t
 *4: 0001 0000: 10 16
 *5: 0010 0000: 20 32
 *6: 0100 0000: 40 64
 *7: 1000 0000: 80 -128
 */