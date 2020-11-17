/* dh.c */

#define USAGE \
"dh [infile [outfile]] [-gmpsu]"

#define HELPTEXT \
"Remove non distance hereditary graphs from a file of graphs.\n\n\
    -g    :  use graph6 output\n\
    -m    :  use adjacency matrix output\n\
    -p    :  use pg output\n\
    -s    :  use sparse6 output\n\
    -u    :  do not output graphs\n\
    -z    :  use tkz-berge.sty output\n\
\n"

#ifndef MAXN
#define MAXN 32
#endif

#if MAXN > 32
#error "Can't have MAXN greater than 32"
#endif

#define ONE_WORD_SETS
#include "gtools.h"

#if MAXN < 32
typedef int xword;
#else
typedef unsigned int xword;
#endif

/**************************************************************************/
/**************************************************************************/

int main(int argc, char *argv[])
{
    int i, j, m, n, argnum, codetype, cy, di1, di2, gi,
        maxc1, maxc2, maxd1, maxd2, minc1, minc2, mind1, mind2, ra1, ra2;
    char *arg, sw, *gstr, *hstr, *infilename, *outfilename;
    FILE *infile, *outfile;
    boolean badargs, quiet, gswitch, mswitch, pswitch, sswitch, uswitch,
            zswitch, iso, eul1, eul2;
    unsigned long e1, e2;
    long long numread, numwritten, st;
    double t;
    graph *g, gc[MAXN*MAXM], hc[MAXN*MAXM];
    set *s1, *s2;

    HELP;
    badargs = quiet = gswitch = mswitch = pswitch = sswitch = uswitch
            = zswitch = FALSE;
    infilename = outfilename = NULL;
    argnum = numread = numwritten = 0;
    for (i = 1; !badargs && i < argc; ++i)
    {
        arg = argv[i];
        if (arg[0] == '-' && arg[1] != '\0')
        {
            ++arg;
            while (*arg != '\0')
            {
                sw = *arg++;
                SWBOOLEAN('q', quiet)
                else SWBOOLEAN('g', gswitch)
                else SWBOOLEAN('m', sswitch)
                else SWBOOLEAN('p', pswitch)
                else SWBOOLEAN('s', sswitch)
                else SWBOOLEAN('u', uswitch)
                else SWBOOLEAN('z', zswitch)
                else badargs = TRUE;
            }
        }
        else
        {
            ++argnum;
            if (argnum == 1)
                infilename = arg;
            else if (argnum == 2)
                outfilename = arg;
            else badargs = TRUE;
        }
    }
    if (gswitch + mswitch + pswitch + sswitch + uswitch + zswitch > 1)
        gt_abort(">E dh: -gmpsuz are incompatible\n");
    if (badargs)
    {
        fprintf(stderr, ">E Usage: %s\n", USAGE);
        GETHELP;
        exit(1);
    }
    if (!quiet)
    {
        fprintf(stderr, ">A dh");
        if (sswitch || gswitch)
            fprintf(stderr, " -");
        if (sswitch)
            fprintf(stderr, "s");
        if (gswitch)
            fprintf(stderr, "g");
        if (argnum > 0)
            fprintf(stderr, " %s", infilename);
        if (argnum > 1)
            fprintf(stderr, " %s", outfilename);
        fprintf(stderr, "\n");
    }
    if (gswitch)
        codetype = GRAPH6;
    else codetype = SPARSE6;
    if (infilename && infilename[0] == '-')
        infilename = NULL;
    infile = opengraphfile(infilename, &codetype, FALSE, 1);
    if (!infile)
        exit(1);
    if (!infilename)
        infilename = "stdin";
    if (!outfilename || outfilename[0] == '-')
    {
        outfilename = "stdout";
        outfile = stdout;
    }
    else if ((outfile = fopen(outfilename, "w")) == NULL)
    {
        fprintf(stderr, "Can't open output file %s\n", outfilename);
        gt_abort(NULL);
    }

    if (!quiet)
        fprintf(stderr, ">Z Reading graphs from %s\n", infilename);
    for (t = CPUTIME; ; free(g))
    {
        if (++numread % 1000000 == 0)
            fprintf(stderr, ">%llu graphs checked\n", numread);
        if ((g = readg(infile, NULL, 0, &m, &n)) == NULL)
            break;
        if (!isconnected(g, m, n) || !distance_hereditary(g, m, n))
            continue;
        fcanonise(g, m, n, gc, NULL, FALSE);
        if (mswitch)
            writeadj(outfile, gc, n);
        else if (pswitch)
            writepg(outfile, gc, n);
        else if (zswitch)
            writetkz(outfile, gc, n);
        else if (!uswitch)
            writeg6(outfile, gc, 1, n);
        fflush(outfile);
        ++numwritten;
    }
    if (!quiet)
        fprintf(stderr, ">Z %llu graphs written to %s in %f seconds\n",
                numwritten, outfilename, CPUTIME - t);

    return EXIT_SUCCESS;
}
