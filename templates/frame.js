// Internal Frame type
function Frame(rows, cols, duration) {
    this.rows = rows;
    this.cols = cols;
    this.duration = duration;
    this.data = new Array();

    
    for (var row = 0; row < rows; ++row) {
        t = new Array();
        for (var col = 0; col < cols; ++col) {
            var color = new Color(0, 0, 0);
            t.push(color);
        }
        this.data.push(t);
    }

    return this;
}

Frame.prototype = {
    color: function(row, col) {
        return this.data[row][col];
    },
    set_color: function(row, col, color) {
        this.data[row][col] = color;
    },
    // TODO: Handle non 3 color values
    to_xml: function() {
        var frame = $('<__frame></__frame>');
        frame.attr('duration', this.duration);
        
        for (var row = 0; row < this.rows; ++row) {
            var line = '';
            for (var col = 0; col < this.cols; ++col) {
                var color = this.data[row][col].to_string();
                line += color.substr(1, color.length-1);
            }
            line = '<row>'+line+'</row>';
            frame.append(line);
        }

        return frame;
    },
    copy: function() {
        var f = new Frame(this.rows, this.cols, this.duration);
        for (var row = 0; row < this.rows; ++row) {
            for (var col = 0; col < this.cols; ++col) {
                f.set_color(row, col,
                            this.color(row, col).copy());
            }
        }
        return f; 
    }
};

// Concrete xml based frame implementation
function XmlFrame(rows, cols, depth, channels) {
    this.rows = rows;
    this.cols = cols;
    this.depth = depth;
    this.channels = channels;

    return this;
}

XmlFrame.prototype = {
    load_xml: function(f) {
        this.frame_xml = $(f);
        this.duration = parseInt(this.frame_xml.attr('duration'));
        return this;
    },
    colorFromString: function(row_str, col) {
        var c = new Color(0, 0, 0);
        c.set_from_string('#'+row_str.textContent.substr(this.depth*this.channels/4*col, this.depth*this.channels/4));
        return c;
    },
    to_frame: function() {
        fpletz = new Frame(this.rows, this.cols, this.duration);
        var xf = this;

        fpletz.data = [];        // fpletz
        this.frame_xml.find('row').each(function(i) {
            var t = [];
            for(var col = 0; col < xf.cols; ++ col) {
                t.push(xf.colorFromString(this, col));
            }
            fpletz.data.push(t);
        });

        return fpletz;
    }
};