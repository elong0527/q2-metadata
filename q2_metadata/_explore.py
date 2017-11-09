def design_plog(metadata: qiime2.Metadata,
                individual_id_column: str,
                individual_time_column: str,
                individual_group_column: str,
                fig_width: int,
                fig_height: int):

  # load and prep metadata
  metadata = _load_metadata(metadata)
  _validate_metadata_is_superset(metadata, table)
  metadata = metadata[metadata.index.isin(table.index)]
  
  # validate id column  (#How could I ensure, time column is a int/numeric?)
  _validate_input_columns(metadata, individual_id_column, None, None, None)
  _validate_input_columns(metadata, individual_time_column, None, None, None)
  _validate_input_columns(metadata, individual_group_column, None, None, None)
  
  _design_plot(sample_md, individual_id_column, individual_time_column,
               individual_group_column, fig_width, fig_height)


def _design_plot(sample_md,
                 individual_id_column,
                 individual_time_column,
                 individual_group_column,
                 fig_width,
                 fig_height):
    '''Function to create study design plot.
    sample_md: pd.DataFrame
        Sample metadata
    individual_id_column: str
        Metadata column containing IDs for individual subjects
    individual_time_column: str
        Metadata column containing sample collection time for individual subjects
    individual_group_column: str
        Metadata column containing group indicator of individual subjects
    fig_width: int
        Figure Width
    fig_height: int
        Figure Height
    '''

    sample_md = sample_md.rename(columns={individual_id_column: 'id',
                                  individual_time_column: 'time',
                                  individual_group_column: 'group'})

    sample_md["id_loc"] = sample_md["id"].astype('category').cat.codes
    # Keep for potential operation of the label
    sample_md["id_label"] = sample_md["id"]

    u_group = sample_md["group"].unique()
    n_group = len(u_group)
    sample_md_meta = sample_md[["id", "id_loc", "id_label"]]
    sample_md_meta = sample_md_meta.drop_duplicates().reset_index(drop=True)

    plt.figure(figsize=(fig_width, fig_height))

    for i, grp in enumerate(u_group):
        _md = sample_md[sample_md.group == grp]
        plt.scatter(_md.time, _md.id_loc, label = grp)

    plt.xlabel(individual_time_column)
    plt.yticks(sample_md_meta["id_loc"], sample_md_meta["id_label"])
    plt.ylabel(individual_id_column)
    plt.legend(loc=9, bbox_to_anchor = (0.5, -0.1), ncol = n_group)
