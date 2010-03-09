    var antibiotics = [
  { bacteria: "Mycobacterium tuberculosis", penicillin: 800, streptomycin: 5, neomycin: 2, gram: "negative" },
  { bacteria: "Salmonella schottmuelleri", penicillin: 10, streptomycin: 0.8, neomycin: 0.09, gram: "negative" },
  { bacteria: "Proteus vulgaris", penicillin: 3, streptomycin: 0.1, neomycin: 0.1, gram: "negative" },
  { bacteria: "Klebsiella pneumoniae", penicillin: 850, streptomycin: 1.2, neomycin: 1, gram: "negative" },
  { bacteria: "Brucella abortus", penicillin: 1, streptomycin: 2, neomycin: 0.02, gram: "negative" },
  { bacteria: "Pseudomonas aeruginosa", penicillin: 850, streptomycin: 2, neomycin: 0.4, gram: "negative" },
  { bacteria: "Escherichia coli", penicillin: 100, streptomycin: 0.4, neomycin: 0.1, gram: "negative" },
  { bacteria: "Salmonella (Eberthella) typhosa", penicillin: 1, streptomycin: 0.4, neomycin: 0.008, gram: "negative" },
  { bacteria: "Aerobacter aerogenes", penicillin: 870, streptomycin: 1, neomycin: 1.6, gram: "negative" },
  { bacteria: "Brucella antracis", penicillin: 0.001, streptomycin: 0.01, neomycin: 0.007, gram: "positive" },
  { bacteria: "Streptococcus fecalis", penicillin: 1, streptomycin: 1, neomycin: 0.1, gram: "positive" },
  { bacteria: "Staphylococcus aureus", penicillin: 0.03, streptomycin: 0.03, neomycin: 0.001, gram: "positive" },
  { bacteria: "Staphylococcus albus", penicillin: 0.007, streptomycin: 0.1, neomycin: 0.001, gram: "positive" },
  { bacteria: "Streptococcus hemolyticus", penicillin: 0.001, streptomycin: 14, neomycin: 10, gram: "positive" },
  { bacteria: "Streptococcus viridans", penicillin: 0.005, streptomycin: 10, neomycin: 40, gram: "positive" },
  { bacteria: "Diplococcus pneumoniae", penicillin: 0.005, streptomycin: 11, neomycin: 10, gram: "positive" }
];


      /* Basic dimensions. */
      var width = 700;
      var height = 700;
      var innerRadius = 90;
      var outerRadius = 300 - 10;

      /* Colors. */
      var drugColor = {
          Penicillin: "rgb(10, 50, 100)",
          Streptomycin: "rgb(200, 70, 50)",
          Neomycin: "black"
        }, gramColor = {
          positive: "rgba(174, 174, 184, .8)",
          negative: "rgba(230, 130, 110, .8)"
        };

      /* Burtin's radius encoding is, as far as I can tell, sqrt(log(mic)). */
      var min = Math.sqrt(Math.log(.001 * 1E4));
      var max = Math.sqrt(Math.log(1000 * 1E4));
      var a = (outerRadius - innerRadius) / (min - max);
      var b = innerRadius - a * max;
      function radius(mic) a * Math.sqrt(Math.log(mic * 1E4)) + b;

      /*
       * The pie is split into equal sections for each bacteria, with a blank
       * section at the top for the grid labels. Each wedge is further
       * subdivided to make room for the three antibiotics, equispaced.
       */
      var bigAngle = 2.0 * Math.PI / (antibiotics.length + 1);
      var smallAngle = bigAngle / 7;

      /* The root panel. */
      var vis = new pv.Panel()
          .width(width)
          .height(height)
          .bottom(100);

      /* Background wedges to indicate gram staining color. */
      var bg = vis.add(pv.Wedge)
          .data(antibiotics) // assumes Burtin's order
          .left(width / 2)
          .top(height / 2)
          .innerRadius(innerRadius)
          .outerRadius(outerRadius)
          .angle(bigAngle)
          .startAngle(function(d) this.index * bigAngle + bigAngle / 2 - Math.PI / 2)
          .fillStyle(function(d) gramColor[d.gram]);

      /* Antibiotics. */
      bg.add(pv.Wedge)
          .angle(smallAngle)
          .startAngle(function(d) this.proto.startAngle() + smallAngle)
          .outerRadius(function(d) radius(d.penicillin))
          .fillStyle(drugColor.Penicillin)
        .add(pv.Wedge)
          .startAngle(function(d) this.proto.startAngle() + 2 * smallAngle)
          .outerRadius(function(d) radius(d.streptomycin))
          .fillStyle(drugColor.Streptomycin)
        .add(pv.Wedge)
          .outerRadius(function(d) radius(d.neomycin))
          .fillStyle(drugColor.Neomycin);

      /* Circular grid lines. */
      bg.add(pv.Dot)
          .data(pv.range(-3, 4))
          .fillStyle(null)
          .strokeStyle("#eee")
          .lineWidth(1)
          .size(function(i) Math.pow(radius(Math.pow(10, i)), 2))
        .anchor("top").add(pv.Label)
          .visible(function(i) i < 3)
          .textBaseline("middle")
          .text(function(i) Math.pow(10, i).toFixed((i > 0) ? 0 : -i));

      /* Radial grid lines. */
      bg.add(pv.Wedge)
          .data(pv.range(antibiotics.length + 1))
          .innerRadius(innerRadius - 10)
          .outerRadius(outerRadius + 10)
          .fillStyle(null)
          .strokeStyle("black")
          .angle(0);

      /* Labels. */
      bg.anchor("outer").add(pv.Label)
          .textAlign("center")
          .text(function(d) d.bacteria);

      /* Antibiotic legend. */
      vis.add(pv.Bar)
          .data(pv.keys(drugColor))
          .right(width / 2 + 3)
          .top(function() height / 2 - 28 + this.index * 18)
          .fillStyle(function(d) drugColor[d])
          .width(36)
          .height(12)
        .anchor("right").add(pv.Label)
          .textMargin(6)
          .textAlign("left");

      /* Gram-stain legend. */
      vis.add(pv.Dot)
          .data(pv.keys(gramColor))
          .left(width / 2 - 20)
          .bottom(function() -60 + this.index * 18)
          .fillStyle(function(d) gramColor[d])
          .strokeStyle(null)
          .size(30)
        .anchor("right").add(pv.Label)
          .textMargin(6)
          .textAlign("left")
          .text(function(d) "Gram-" + d);

      vis.render();