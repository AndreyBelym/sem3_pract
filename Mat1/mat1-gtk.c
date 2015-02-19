#include <gtk/gtk.h>
#include <stdio.h>
void open_file(char *filename){
	printf("file opened!\n");
}
GtkBuilder              *builder;

void 
on_window1_destroy (GtkObject *object, gpointer user_data)
{
        gtk_main_quit();
}
void* thread_0(void *args){
	long i;
	gdk_threads_enter();
	gtk_spinner_start(GTK_SPINNER(args));
	gdk_threads_leave();
	for (i=0;i<500000;++i) {
		printf("%ld,\n",i);
		};
	gdk_threads_enter();
	gtk_spinner_stop(GTK_SPINNER(args));
	gdk_threads_leave();
	return NULL;
}
void
on_tlbCalc_clicked(GtkObject *object, gpointer user_data)
{
	GtkProgressBar *progress;
	GtkWidget *spin;
	gboolean spin_active;
	
	

	progress=GTK_PROGRESS_BAR(gtk_builder_get_object (builder, "progressbar1"));
	spin = GTK_WIDGET(gtk_builder_get_object (builder, "spinner1"));
	gtk_progress_bar_pulse(progress);
	g_thread_create(&thread_0,spin,FALSE,NULL);

}


void 
on_tlbOpen_clicked(GtkObject *object, gpointer user_data)
{
        GtkWidget *dialog;
		dialog = GTK_WIDGET(gtk_builder_get_object (builder, "filechooserdialog1"));
		if (gtk_dialog_run (GTK_DIALOG (dialog)) == GTK_RESPONSE_ACCEPT)
  		{
    		char *filename;
    		filename = gtk_file_chooser_get_filename (GTK_FILE_CHOOSER (dialog));
    		open_file (filename);
    		//g_free (filename);
  		}
	g_object_unref(G_OBJECT(dialog));
}

int
main (int argc, char *argv[])
{
        GtkWidget               *window;
        
		g_thread_init(NULL);
  		gdk_threads_init();

        gtk_init (&argc, &argv);
        
        builder = gtk_builder_new ();
        gtk_builder_add_from_file (builder, "interface.glade", NULL);

        window = GTK_WIDGET (gtk_builder_get_object (builder, "window1"));
        //g_signal_connect (window, "destroy", G_CALLBACK (gtk_main_quit), NULL);
		gtk_builder_connect_signals (builder, NULL);          
        //g_object_unref (G_OBJECT (builder));
        
        gtk_widget_show (window);       
        
		gdk_threads_enter();
		gtk_main ();
        gdk_threads_leave();

        return 0;
}
