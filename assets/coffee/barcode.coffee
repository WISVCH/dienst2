# Barcode JS
angular
  .module('kas.barcode', [])
  .factory('Barcode', () ->

    groups = ['OOOOOO','OOEOEE','OOEEOE','OOEEEO','OEOOEE','OEEOOE','OEEEOO','OEOEOE','OEOEEO','OEEOEO'];
    encodings = {
      'O' : ['0001101','0011001','0010011','0111101','0100011','0110001','0101111','0111011','0110111','0001011'],
      'E' : ['0100111','0110011','0011011','0100001','0011101','0111001','0000101','0010001','0001001','0010111'],
      'R' : ['1110010','1100110','1101100','1000010','1011100','1001110','1010000','1000100','1001000','1110100']
    }

    withChecksum = (num) ->
      # Initialize the array
      array = [0,0,0,0,0,0,0,0,0,0,0,0];

      for i in [0..Math.min(num.length, array.length)-1]
        array[i] = parseInt(num.charAt(i))

      # Calculate the checksum
      checksum = 0
      for i in [0..11]
        mul = if (i%2 == 0) then 1 else 3
        checksum += array[i] * mul

      # Add the checksum to the barcode
      array[12] = (Math.ceil(checksum / 10) * 10) - checksum
      array

    encode = (array) ->
      group = groups[array[0]] # Determine the group
      barcode = 'L0L' # Add the Start Sentinel
      
      # Add the first data part
      for i in [1..6]
        barcode += encodings[group.charAt(i-1)][array[i]]
      
      barcode += '0L0L0' # Add the Center Guard
      
      # Add the second data part
      for i in [7..12]
        barcode += encodings['R'][array[i]]

      barcode += 'L0L' # Add the End Sentinel
      barcode

    Barcode = (num, description) -> 
      this.num = num
      this.description = description
      this.withChecksum = withChecksum(num)
      console.log this.withChecksum
      this.encoded = encode(this.withChecksum)
      
    Barcode.create = (num, text) ->
      new Barcode(num, text)

    Barcode.prototype.draw = (canvas) ->  
      canvas.reset()

      margin_left = 25
      margin_top = 22
      margin_bottom = 40

      canvas_width = canvas.width
      canvas_height = canvas.height

      if window.devicePixelRatio
        canvas_width = canvas.width / window.devicePixelRatio
        canvas_height = canvas.height / window.devicePixelRatio

      canvas_width -= margin_left

      bitWidth = Math.floor(canvas_width/this.encoded.length)

      console.log this.encoded.length

      barcodeHeight = canvas_height - margin_top

      for i in [0..this.encoded.length-1]
        bit = this.encoded.charAt(i)

        bitHeight = barcodeHeight - margin_bottom
        if bit == "L"
          bitHeight = barcodeHeight

        if bit != "0"
          rectangle = canvas.display.rectangle({
            x: i * bitWidth + margin_left,
            y: margin_top,
            width: bitWidth,
            height: bitHeight,
            fill: "#000"
          })
          canvas.addChild(rectangle)

      basetext = {
        x: 0,
        y: canvas_height - margin_bottom,
        font: "33px monospace",
        fill: "#000"
      }

      desc = angular.extend({}, basetext, {text: this.description, y: 0, font: "20px bold Arial"})
      canvas.addChild(canvas.display.text(desc))

      num1 = angular.extend({}, basetext, {text: this.withChecksum.join('').substring(0, 1)})
      canvas.addChild(canvas.display.text(num1))

      num2 = angular.extend({}, basetext, {text: this.withChecksum.join('').substring(1, 7), x: 5 * bitWidth + margin_left})
      canvas.addChild(canvas.display.text(num2))

      num3 = angular.extend({}, basetext, {text: this.withChecksum.join('').substring(7, 13), x: 50 * bitWidth + margin_left})
      canvas.addChild(canvas.display.text(num3))

    Barcode
  )

#   // Draw the text
#   canvas.drawText({
#       fillStyle: "#000",
#       x: 0, y: 0,
#       font: "14pt Monaco",
#       text: text,
#       fromCenter: false,
#   });

#   canvas.drawText({
#       fillStyle: "#000",
#       x: 0, y: 130,
#       font: "14pt Monaco",
#       text: barcode[0],
#       fromCenter: false,
#   });

#   canvas.drawText({
#       fillStyle: "#000",
#       x: 35, y: 130,
#       font: "14pt Monaco",
#       text: barcode.join('').substring(1,7),
#       fromCenter: false,
#   });

#   canvas.drawText({
#       fillStyle: "#000",
#       x: 130, y: 130,
#       font: "14pt Monaco",
#       text: barcode.join('').substring(7,13),
#       fromCenter: false,
#   });
# }