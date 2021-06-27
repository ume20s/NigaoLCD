import time, wiringpi as pi, binascii

class sc1602:
	def __init__( self, RS, E, D4, D5, D6, D7 ):
		self.RS = RS
		self.E = E
		self.D4 = D4
		self.D5 = D5
		self.D6 = D6
		self.D7 = D7
		
		self.LCD_LINE1 = 0x80
		self.LCD_LINE2 = 0xC0
		
		self.E_PULSE = 0.0005
		self.E_DELAY = 0.0005
		
		self.B_CURSOL = 0
		self.C_CURSOL = 0
		
		self.X =0
		self.Y =0
		
		pi.pinMode( self.RS, 1 )
		pi.pinMode( self.E, 1 )
		pi.pinMode( self.D4, 1 )
		pi.pinMode( self.D5, 1 )
		pi.pinMode( self.D6, 1 )
		pi.pinMode( self.D7, 1 )
		
		self.allpin_low()
		
		self.setup( )
	
	def setup( self ):
		self.lcd_byte( 0x33, 0 )
		self.lcd_byte( 0x32, 0 )
		self.lcd_byte( 0x06, 0 )
		self.set_cursol( 0 )
		self.set_blink( 1 )
		self.lcd_byte( 0x28, 0 )
		self.clear( )
		self.move_home( )

	def allpin_low( self ):
		pi.digitalWrite( self.RS, 0 )
		pi.digitalWrite( self.E, 0 )
		pi.digitalWrite( self.D4, 0 )
		pi.digitalWrite( self.D5, 0 )
		pi.digitalWrite( self.D6, 0 )
		pi.digitalWrite( self.D7, 0 )
	
	def lcd_byte( self, bits, mode ):
		pi.digitalWrite( self.RS, mode )
		
		# High bits
		pi.digitalWrite( self.D4, 0 )
		pi.digitalWrite( self.D5, 0 )
		pi.digitalWrite( self.D6, 0 )
		pi.digitalWrite( self.D7, 0 )
		
		pi.digitalWrite( self.D4, bits & 0x10 )
		pi.digitalWrite( self.D5, bits & 0x20 )
		pi.digitalWrite( self.D6, bits & 0x40 )
		pi.digitalWrite( self.D7, bits & 0x80 )
		self.lcd_enable()

		# Low bits
		pi.digitalWrite( self.D4, 0 )
		pi.digitalWrite( self.D5, 0 )
		pi.digitalWrite( self.D6, 0 )
		pi.digitalWrite( self.D7, 0 )
		
		pi.digitalWrite( self.D4, bits & 0x01 )
		pi.digitalWrite( self.D5, bits & 0x02 )
		pi.digitalWrite( self.D6, bits & 0x04 )
		pi.digitalWrite( self.D7, bits & 0x08 )
		self.lcd_enable()		
		
		
	def lcd_enable( self ):
		time.sleep( self.E_DELAY )
		pi.digitalWrite( self.E, 1 )
		time.sleep( self.E_PULSE )
		pi.digitalWrite( self.E, 0 )
		time.sleep( self.E_DELAY )
	
	def set_cursol( self, mode ):
		self.C_CURSOL = mode
		buf = 0x0c + ( 0x02 * self.C_CURSOL ) + ( 0x01 * self.B_CURSOL )
		self.lcd_byte( buf, 0 )

	def set_blink( self, mode ):
		self.B_CURSOL = mode
		buf = 0x0c + ( 0x02 * self.C_CURSOL ) + ( 0x01 * self.B_CURSOL )
		self.lcd_byte( buf, 0 )

	def clear( self ):
		self.lcd_byte( 0x01, 0 )
	
	def move( self, x, y ):
		self.X = x
		self.Y = y
		if self.X < 0:
			self.X = 0
		if self.X > 0x0f:
			self.X = 0x0f
		if self.Y < 0:
			self.Y = 0
		if self.Y > 1:
			self.Y = 1
		oy = self.Y * 0x40
		buf = self.X + oy + 0x80
		self.lcd_byte( buf, 0 )

	def move_home( self ):
		self.move( 0, 0 )

	def write( self, buf ):
		length = len(buf)
		i = 0
		while i < length:
			if self.X > 0x0f:
				if self.Y == 0:
					self.move( 0x00, 0x01 )
				else:
					break
			self.lcd_byte( ord( buf[i] ), 1 )
			
			self.X = self.X + 1
			i = i + 1

