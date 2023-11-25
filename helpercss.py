def create_tooltip(title, description):
    tooltip_html = f"""
    <div class="tooltip">{title}
      <span class="tooltiptext">{description}</span>
    </div>

    <style>
    .tooltip {{
      position: relative;
      display: inline-block;
      border-bottom: 1px dotted black; /* Dotted underline for the tooltip */
    }}

    .tooltip .tooltiptext {{
      visibility: hidden;
      width: 200px;
      background-color: black;
      color: #fff;
      text-align: center;
      border-radius: 6px;
      padding: 5px 5px;
      position: absolute;
      z-index: 1;
      top: 30px; /* Position below the tooltip */
      left: 0%;
      opacity: 0;
      transition: opacity 0.3s;
    }}

    .tooltip:hover .tooltiptext {{
      visibility: visible;
      opacity: 1;
    }}
    </style>
    """
    return tooltip_html
